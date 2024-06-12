from com.dtmilano.android.viewclient import ViewClient
import subprocess

def is_box_checked(view_client: ViewClient, id_str: str) -> bool:
    view = view_client.findViewById(id_str)
    return view is not None and view.checked()

def music_player_permissions_for_old_android_version(view_client: ViewClient):
    # check if the permission dialog is shown
    allow_button = view_client.findViewWithText('ALLOW')
    if allow_button is not None:
        allow_button.touch()
    view_client.dump()
    pass

def music_player_restore_playlist_functioning(view_client: ViewClient):
    # restore the playlist functioning
    view_dict = view_client.getViewsById()
    for k in view_dict.keys():
        view = view_dict[k]
        if view.map['resource-id'] == 'com.simplemobiletools.musicplayer:id/tab_item_label':
            if view.text().lower() == 'albums':
                view.touch()
                view_client.dump()
                break
    pass

def recorder_permissions_for_old_android_version(view_client: ViewClient):
    # check if the permission dialog is shown
    allow_button = view_client.findViewWithText('ALLOW')
    if allow_button is not None:
        allow_button.touch()
    view_client.dump()
    pass

def filemanager_permissions(view_client: ViewClient):
    OK_button = view_client.findViewWithText('OK')
    if OK_button is not None:
        OK_button.touch()
        view_client.dump()
        allow_access = view_client.findViewWithText('Allow access to manage all files')
        allow_access.touch()
        view_client.dump()
        navigate_up = view_client.findViewWithContentDescription('Navigate up')
        navigate_up.touch()
        view_client.dump()
        return 
    else:
        return 
    
def filemanager_delete_all_files_under_folder(view_client: ViewClient):
    subprocess.run(['adb', 'shell', 'rm', '-rf', '/sdcard/Download/*'])

def filemanager_create_file_under_download(view_client: ViewClient, filename='Testfile.txt'):
    # create a file called 'Testfile.txt' under the 'Download' folder  
    view_client.dump()
    if view_client.findViewWithText('> Download') is None:
        download_folder = view_client.findViewWithText('Download')
        if download_folder is None:
            raise RuntimeError("Failed to navigate in to Download")
        download_folder.touch()
    view_client.dump()
    create_file_button = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/items_fab')
    create_file_button.touch()
    view_client.dump()
    file_title = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/item_title')
    file_title.setText(filename)
    File_button = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/dialog_radio_file')
    File_button.touch()
    Ok_button = view_client.findViewWithText('OK')
    Ok_button.touch()
    return

def messager_delete_all(view_client):
    print("teardown sms...")
    pkg = "com.simplemobiletools.smsmessenger"
    view_client.device.forceStop(package=pkg)
    view_client.device.startActivity(package=pkg)

    view_client.dump()
    # delete the new conversation we started
    # use a while loop to delete all possible messages
    messageView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/conversation_address')
    while messageView is not None:
        messageView.longTouch()
        view_client.dump()
        deleteView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/cab_delete')
        deleteView.touch()
        view_client.dump()
        yesView = view_client.findViewWithText('Yes')
        yesView.touch()
        view_client.dump()
        messageView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/conversation_address')
    pass

def recorder_delete_all():
    subprocess.run(['adb', 'shell', 'rm', '-rf', '/sdcard/Music/Recordings/*'])

def disable_app(package_name):
    command = ["adb", "shell", "pm", "disable-user", "--user", "0", package_name]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Disabled {package_name}:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code for {package_name}:", e.returncode)
        print("Error output:", e.stderr)
    except Exception as e:
        print(f"An error occurred while disabling {package_name}:", str(e))