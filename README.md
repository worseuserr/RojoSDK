# RojoSDK

A simple, dependency-aware SDK for `Rojo` projects.

[![License](https://img.shields.io/badge/license-MIT-blue)](./.sdk/LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.1-informational)](./build.config.toml)

**RojoSDK** simplifies project development by managing dependencies as Git submodules and merging all source files into a single, clean `build/` directory, keeping your work-in-progress code separate from the live version.

## Key Features

-   **Decoupled Workflow:** Work safely in `src/` while `Rojo` streams the stable `build/` directory. This prevents half-written or broken code from affecting your running instance.
-   **Unified Build Directory:** Merges your project's `src/` with the source folders of all dependencies into a single `build/` output.
-   **Git Submodule Dependencies:** Manages project dependencies declared in `build.config.toml` as Git submodules in the `lib/` directory.
-   **Recursive Builds:** Automatically detects and builds dependencies that also use **RojoSDK**, ensuring you always use their latest build output.
-   **Declarative Configuration:** All build settings, dependencies, and update policies are managed in a simple `build.config.toml` file.
-   **Simple CLI:** A straightforward command-line interface for building, cleaning, and managing your project.
-   **Multi-platform:** Natively supports any platform with **Python 3.12+** and **Git** installed.

## Getting Started

1.  **Download the latest version from releases.**
    Make sure you have at least **Python 3.12+** installed to run the build script. And **Git**, obviously.

2.  **Extract and configure:**
    Open `build.config.toml` and configure the settings to your liking. It is recommended to add your project's dependencies before the next step.

3.  **Run the initial build script:**
    This command will configure everything and install any dependencies listed in `build.config.toml`.
    ```sh
    python3 build.py -N
    ```
	The `-N` option causes the script to not perform the build process after setup. It's optional, but useful if you don't immediately want to build the dependencies.

4.  **Start developing!**
    Your project source code goes in `src/`, and the combined output will appear in `build/` after every run.
    Serve `build.project.json` to `Rojo` and all your build files will be synced.

## How It Works

The core function of the build script is to create a unified `build/` directory by intelligently merging source files, while also stopping unfinished `src/` code from preventing debugging.

The script scans your `src/` directory and all dependency directories inside `lib/`. It then copies their contents into the `build/` folder, maintaining the original folder structure.

**Key Rule:** If a dependency in `lib/` contains its own `build.py` script, that script is run first, and its `build/` folder is used as the source. Otherwise, its `src/` folder is used.

### Example File Structure

**Input:**
```
- /MyNewProject
   - /src
      - /ReplicatedStorage
         - SmoothCamera.lua
   - /lib
      - /MyLibrary
         - /src
            - /ReplicatedStorage
               - BaseCamera.lua
```

**Output of `python3 build.py`:**
```
- /MyNewProject
   - /build
      - /ReplicatedStorage
         - BaseCamera.lua
         - SmoothCamera.lua
```

## Command-Line Usage

The build script features a powerful CLI for full customization without needing to edit the config file.

```
Usage: python3 build.py [OPTIONS]
   -V, --version       Show the version and exit
   -h, --help          Show this message and exit
   -s, --skip-setup    Skip first-build setup (only use if you know what you are doing)
   -f, --force-setup   Force first-build setup to run before building
   -v, --verbose       Enable more verbose output
   -r, --reset         Full clean and rerun setup
   -N, --no-clean      Disable automatically cleaning missing/trailing files and git entries
   -F, --full-clean    Clean everything, including build and lib folders (destructive, back to pre-setup state)
   -n, --no-build      Don't start build process
```

## Configuration (`build.config.toml`)

All project settings are managed in the `build.config.toml` file.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License - see the [LICENSE](./.sdk/LICENSE) file for details.
