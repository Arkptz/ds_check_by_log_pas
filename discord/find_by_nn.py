import os
list_dirs = [r'E:\Рабочий стол\ss\discord_checker_by_log_pas\test_df\Lib\site-packages\discord','A:\Anaconda\Lib\site-packages\discord', 'A:/Anaconda/Lib/site-packages/discord/types', 'A:\Anaconda\Lib\site-packages\discord\ext\commands']
for dir in list_dirs:
    arr = os.listdir(dir)
    for file in arr:
        if not '.py' in file:
            continue
        else:
            with open(f'{dir}\{file}', 'r', encoding='utf-8') as files:
                a = files.read()
                if 'on_required_action_update' in a:
                    print(file)