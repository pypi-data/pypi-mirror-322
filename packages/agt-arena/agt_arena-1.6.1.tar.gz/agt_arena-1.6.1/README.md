# CS410 Arena

A Go game arena for running bot competitions in CS1440.

## Running the Arena

Given that the submission files are in the `submissions` director (presumably from the autograder script),  
here's what you need to do to run the arena:  
Note: Some of this is still in development, so the instructions may change as I refine this in the future.  

1. CD into submissions/shared and build the base Dockerfile as cs1440base by running:  

    ```bash
    docker build -f BaseDockerfile -t cs1440base .
    ```

2. Update the corresponding config in go_config to match what settings you want to run.

3. CD back out to the root of the directory and run the following command:  

    ```bash
    docker network create tournament
    docker compose --env-file configs/go_config.env up
    ```

4. The arena should now be running. You can observe the logs in logs and the results in meta after it's done. This will take up a lot of image space depending on the number of submissions so make sure to clean up docker images after you're done.
