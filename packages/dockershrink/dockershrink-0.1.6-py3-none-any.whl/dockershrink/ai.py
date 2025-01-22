import os
from typing import Dict, List

from openai import OpenAI

openai_model = "gpt-4o-2024-08-06"

_multistage_system_prompt = """
You are an expert software and DevOps engineer who specializes in Docker and NodeJS backend applications.

Given a Nodejs project that contains a Docker image definition to containerize it, your goal is to reduce the size of the docker image as much as possible, while still keeping the code legible and developer-friendly.

As part of this request, your only task is to modify the given single-stage Dockerfile to adopt Multistage builds.
Multistage is beneficial because the final image produced (final stage) uses a slim base image and only contains things that we put in it.
Create a final stage in the Dockerfile which only contains the application source code, its dependencies (excluding "devDependencies" from package.json) and anything else you think is necessary for the app at runtime or relevant to the final image.

* The final stage must use a slim base image if possible. If the previous stage uses a specific version of NodeJS, make sure to use the same version.
* If possible, set the `NODE_ENV` environment variable to `production`. This should be done BEFORE running any commands related to nodejs or npm. This ensures that dev dependencies are not installed in the final stage.
* Do a fresh install of the dependencies (node_modules) in the final stage and exclude dev dependencies. Do not change the installation commands in the previous stage and don't copy node_modules from the previous stage.
* Try to keep your code changes as consistent with the original code as possible. For example, if the previous stage uses "npm install" for installing dependencies, don't replace it with "npm ci". Try to use "install" only.
* If the previous stage contains some metadata such as LABEL statements, make sure to include them in the final stage as well, if you think it is relevant.
* Comments should be added only in the new stage that you're writing. Don't add any comments in the previous stage unless you need to make an important remark. But don't remove any comments that already exist.
* If the previous stage contains any `RUN` statements invoking any npm scripts like `npm run build`, the commands in this script will also be shared with you so you can understand its behaviour.
* Do not delete any statements originally present in the Dockerfile. If you don't understand what they're being used for (like custom scripts), just ignore them. Don't include them to the new stage.

After writing all the code, review it step-by-step and think what the final image would contain to ensure you didn't accidentally leave out anything important.

* Return only the Dockerfile code in your reply
* Do not include any additional formatting, such as markdown code blocks
"""

_multistage_user_prompt = """
Optimize this Dockerfile:

```
{dockerfile}
```
"""

_prompt_npm_scripts_invoked = """
-- Details of NPM scripts invoked --

NOTE:
- "script" is the npm script you see in the Dockerfile (eg- "npm run test")
- "commands" is the set of commands defined inside package.json for the particular npm script.
  For example, if package.json is `{"scripts": {"test": "gulp ."}}`, then this field's value will be "gulp ." because the "script" invoked is "test".
- the commands for all npm scripts are extracted from package.json.

LIST OF SCRIPTS:

"""


class AIService:
    _client: OpenAI

    def __init__(self, client: OpenAI):
        self._client = client

    def add_multistage_builds(
        self, dockerfile: str, scripts: List[Dict[str, str]]
    ) -> str:
        user_prompt = _multistage_user_prompt.format(dockerfile=dockerfile)

        if scripts:
            scripts_description = []

            for i in range(len(scripts)):
                script = scripts[i]
                description = f"""{i + 1}. script: `{script["script"]}`
commands: `{script["commands"]}`
"""
                scripts_description.append(description)

            scripts_description = os.linesep.join(scripts_description)
            user_prompt += _prompt_npm_scripts_invoked + scripts_description

        messages = [
            {
                "role": "system",
                "content": _multistage_system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]
        # TODO: Set temperature
        # should be set to a low value, we want more deterministic, fact-based results for our tasks
        completion = self._client.chat.completions.create(
            messages=messages,
            model=openai_model,
        )
        response = completion.choices[0].message.content
        # gpt-4o always returns code inside backticks "```dockerfile...```".
        # We need to scrub them off and return clean dockerfile code.
        response = response.strip().strip("```").strip()

        return response

    def generate_dockerfile(self, package_json_analysis: Dict) -> str:
        """Generate a Dockerfile with dependency validation"""
        system_prompt = """
        You are an expert software and DevOps engineer who specializes in Docker and NodeJS applications.
        Generate an optimized multi-stage Dockerfile that minimizes image size while maintaining functionality.

        Requirements for the Dockerfile:
        * Create a multi-stage build with at least two stages
        * First stage for building/testing (use node:slim)
        * Final stage for production (use node:alpine)
        * Set NODE_ENV=production before npm/yarn commands
        * Install only production dependencies in final stage
        * Copy only necessary files between stages
        * Include LABEL metadata if relevant
        * Add helpful comments explaining each stage

        Build stage must:
        * Copy package*.json first
        * Install all dependencies
        * Copy over application source code
        * Run 'npx depcheck' to verify no unused packages
        * Run build script if present
        * Test the application if test script exists

        Production stage must:
        * Use lightest possible base image
        * Install only production dependencies
        * Copy built artifacts from build stage
        * Set appropriate CMD/ENTRYPOINT
        * Exclude devDependencies and test files

        Return only the Dockerfile content without any formatting or markdown.
        Dockerfile can include comments to explain each stage.
        """

        project_info = f"""
        Package name: {package_json_analysis['name']}
        Entry point: {package_json_analysis['main']}
        Has build script: {package_json_analysis['has_build_script']}
        Has start script: {package_json_analysis['has_start_script']}
        Scripts available: {list(package_json_analysis['scripts'].keys())}
        Dependencies: {list(package_json_analysis.get('dependencies', {}).keys())}
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": project_info,
            },
        ]
        completion = self._client.chat.completions.create(
            messages=messages,
            model=openai_model,
        )
        response = completion.choices[0].message.content
        response = response.strip().strip("```").strip()
        return response

    def generate_dockerignore(self, package_json_analysis: Dict) -> str:
        """
        Generate a .dockerignore file based on the analysis of package.json file.
        """
        system_prompt = """
        You are an expert DevOps engineer specializing in Docker and NodeJS applications.
        Generate a .dockerignore file for a NodeJS application that:
        - Ignores unnecessary files and directories
        - Optimizes the Docker build context
        - No need to have package-lock.json in the .dockerignore file
        - Return only the Dockerignore content without any formatting or markdown.

        """
        project_info = f"""
        Package name: {package_json_analysis['name']}
        Entry point: {package_json_analysis['main']}
        Has build script: {package_json_analysis['has_build_script']}
        Has start script: {package_json_analysis['has_start_script']}
        Scripts available: {list(package_json_analysis['scripts'].keys())}
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": project_info,
            },
        ]
        completion = self._client.chat.completions.create(
            messages=messages,
            model=openai_model,
        )
        response = completion.choices[0].message.content
        response = response.strip().strip("```").strip()
        return response
