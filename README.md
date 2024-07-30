# IUYS (Intelligently Understanding Your Screenshots)

## About

Inspired by [Sam Witteveen](https://github.com/samwit) during his demonstration in Machine Learning Singapore group meetup.
This is a more "software engineering" take on the idea (if you'll allow me) and also to improve my skills relating to application development and GenAI related matters

### Note: This project is developed on a Apple Silicon chip!

## Description

IUYS is a tool that understands your images or screenshots for you to be able perform query and find the relevant results ala "Google Search" style

## Tools Used

Note: lancedb in this usage is an embedded database, once we shut the tooling down it loses all context. We retain context by creating a dump file and loading it back when the tool initializes again

- pyee (Event broker)
- Watchdog (File watcher)
- lancedb (Vector store)
- mlx-vlm (Visual language model framework)

## Flows

### Creation Flow

![Creation Flow](./imgs/creation_flow.png)

## To Do List

### General

- Exception handling
- Convert to CLI based tool
  - Allow to be used by other program as an external sidecar
- Testing
- Changing of saving key-value store

### File watcher

- <s>Receive file creation events and emit to Queue worker</s>
- Filter file event only by images
- Identify file by their checksums to decide whether to perform VLM ops
- Exception handling
- Testing

### Queue Worker

- <s>Receive file creation events from File Watcher</s>
  - <s>Filter any unrelated events</s>
  - <s>Task events to a queue</s>
- Optimization?
- Exception handling
- Testing

### OCU

- <s>Receive new tasks from Queue worker and perform inference</s>

- Allow changing of "list-of-allowed" models via CLI arguements
- Testing
- Optimization
  - Currently the models being loaded into my M3 Pro 36gb RAM consumes 25gb!! <- (YIKES)

### Vector store

- <s>Receive OCU inferences into embeddings and storing it into vector store</s>
- Retrieval pipeline
- Testing
