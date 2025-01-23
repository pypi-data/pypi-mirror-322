import os
import time
from datetime import datetime

from openai import OpenAI

from gmicloud import *


def create_artifact_with_file(client: Client) -> str:
    artifact_manager = client.artifact_manager

    # Create an artifact with a file
    artifact_id = artifact_manager.create_artifact_with_file(
        artifact_name="Llama3.1 8B",
        artifact_file_path="./files/Llama-3.1-8B-Instruct.zip",
        description="This is a test artifact",
        tags=['example', 'test']
    )

    return artifact_id


def create_artifact_from_template(client: Client) -> str:
    artifact_manager = client.artifact_manager

    # Get all artifact templates
    templates = artifact_manager.get_artifact_templates()
    print(templates)
    for template in templates:
        if template.artifact_name == "Llama3.1 8B":
            # Create an artifact from a template
            artifact_id = artifact_manager.create_artifact_from_template(
                artifact_template_id=template.artifact_template_id,
            )

            return artifact_id

    return ""


def create_task_and_start(client: Client, artifact_id: str) -> str:
    artifact_manager = client.artifact_manager
    # Wait for the artifact to be ready
    while True:
        try:
            artifact = artifact_manager.get_artifact(artifact_id)
            print(f"Artifact status: {artifact.build_status}")
            # Wait until the artifact is ready
            if artifact.build_status == BuildStatus.SUCCESS:
                break
        except Exception as e:
            raise e
        # Wait for 2 seconds
        time.sleep(2)
    try:
        task_manager = client.task_manager
        # Create a task
        task = task_manager.create_task(Task(
            config=TaskConfig(
                ray_task_config=RayTaskConfig(
                    ray_version="latest-py311-gpu",
                    file_path="serve",
                    artifact_id=artifact_id,
                    deployment_name="app",
                    replica_resource=ReplicaResource(
                        cpu=24,
                        ram_gb=128,
                        gpu=2,
                    ),
                ),
                task_scheduling=TaskScheduling(
                    scheduling_oneoff=OneOffScheduling(
                        trigger_timestamp=int(datetime.now().timestamp()) + 60,
                        min_replicas=1,
                        max_replicas=10,
                    )
                ),
            ),
        ))

        # Start the task
        task_manager.start_task(task.task_id)
    except Exception as e:
        raise e

    return task.task_id


def call_chat_completion(client: Client, task_id: str):
    task_manager = client.task_manager
    # Wait for the task to be ready
    while True:
        try:
            task = task_manager.get_task(task_id)
            print(f"task status: {task.task_status}")
            # Wait until the task is ready
            if task.task_status == "ready":
                break
        except Exception as e:
            print(e)
            return
        # Wait for 2 seconds
        time.sleep(2)

    if not task.info.endpoint or not task.info.endpoint.strip():
        raise Exception("Task endpoint is not ready yet")

    open_ai = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", task.info.endpoint)
    )
    # Make a chat completion request using the new OpenAI client.
    completion = open_ai.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Translate the sentences to Chinese"},
        ],
        max_tokens=200,
        temperature=0.7
    )

    print(completion.choices[0].message.content)


if __name__ == '__main__':
    # Initialize the Client
    cli = Client()

    # print(cli.artifact_manager.get_all_artifacts())

    # Create an artifact with a file
    # artifact_id = create_artifact_with_file(cli)

    # Create an artifact from a template
    #artifact_id = create_artifact_from_template(cli)
    artifact_id = "cba6db2f-315a-4765-9e94-1e692f7fdb39"

    # Create a task and start it
    task_id = create_task_and_start(cli, artifact_id)

    # Call chat completion
    call_chat_completion(cli, task_id)
