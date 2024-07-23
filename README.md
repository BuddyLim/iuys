# IUYS (Intelligently Understanding Your Screenshots)

## About

Inspired by [Sam Witteveen](https://github.com/samwit) during his demonstration in Machine Learning Singapore group meetup.
This is a more "software engineering" take on the idea (if you'll allow me) and also to improve my skills relating to application development and GenAI related matters

### Note: This project is developed on a Apple Silicon chip!

## Description

IUYS is a tool that understands your images or screenshots for you to be able perform query and find the relevant results ala "Google Search" style

## Tools Used

Note: lancedb and dbm in this usage is ephemeral, once we shut the tooling down it loses all context. We retain context by creating a dump file and loading it back when the tool initializes again

- pyee (Event broker)
- Watchdog (File watcher)
- lancedb (Vector store)
- dbm (Key-value store)
- mlx-vlm (Visual language model framework)

## Flows

### Creation Flow

![Creation Flow](./imgs/creation_flow.png)
