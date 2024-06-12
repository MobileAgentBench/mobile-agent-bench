# MobileAgentBench
An automated benchmark for mobile LLM agents.

## Usage

### Install AndroidStudio

Install [AndroidStudio](https://developer.android.com/studio). AndroidStudio installs other debugging tools for you, such as ADB and Android emulators.

You may need to setup your envrionmnet variables.

```bash
export ANDROID_HOME=~/Library/Android/sdk
export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools"
```

### Download Benchmarking Apps

The default benchmarking tasks use apps from [SimpleMobileTools](https://simplemobiletools.com). Please download and install the following apps to your testing device (Android emulator is preferred). If you're using an Android emulator, you can simply drag and drop the APK files to install.

- Calculator
- Calendar
- Contacts
- FileManager
- Gallery
- AppLauncher
- Messager
- MusicPlayer
- Notes
- Recorder

### Build MobileBenchMark as a Python Library

Clone this repo. Run the following commands to install it as a Python library. So you can use import it in other repos.

```bash
python3 -m pip install --upgrade build
python3 -m build
```

You'll find the `mobile_agent_benchmark-0.0.1-py3-none-any.whl` file under the `dist` folder. Activate your agent's virtual environment, then you can run `pip install mobile_agent_benchmark-0.0.1-py3-none-any.whl` to install the library.

## Dummy Agent

For testing purpose, you can run the `dummy_agent.py` file. It acts as the simplest agent. In a for loop, it does nothing but just sleep for a few seconds. You can simulate what a real agent would do to test if the benchmark can successfully detect tash completion.





