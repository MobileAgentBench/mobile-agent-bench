# start emulator 
# /Users/wangluyuan/Library/Android/sdk/emulator/emulator @Pixel_3a_API_34_extension_level_7_arm64-v8a
# start adb:
# /Users/wangluyuan/Library/Android/sdk/platform-tools/adb -e shell
# download apks
# https://github.com/SimpleMobileTools
# download free music (no copyright issue)
# https://pixabay.com/music/


import time
from mobile_agent_benchmark.task_orchestrator import TaskOrchestrator

orchestrator = TaskOrchestrator(log_dir='/Users/luyuanWang/Documents/research/benchmark/mobile_agent_benchmark/logs')


def dummy_agent(prompt):
    print("Agent running task:", prompt)
    for i in range(10):
        print("step", i, "Please execute your action")
        orchestrator.before_one_action()
        time.sleep(3)
        print("Please wait!")
        should_stop = orchestrator.after_one_action("agent step")
        if should_stop:
            break
    print("agent done")
    

if __name__ == '__main__':
    orchestrator.run(dummy_agent)

    