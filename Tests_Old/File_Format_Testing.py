import shutil

import yaml

import Runner


def run(config_name, num_trials):
    with open("{}.yaml".format(config_name), "r") as f:
        config_file = yaml.safe_load(f)
        filename = config_file.get("FILE_NAME")
    Runner.runner(filename, config_name, num_trials)
    shutil.rmtree("Files")
    shutil.rmtree("Files_Read")


if __name__ == "__main__":
    # Create configuration file if it does not exist.
    # check = int(input("Would you like a sample configuration file to be generated? Press 1 for yes and 2 for no.\n"))
    # if check == 1:
    #     data = {
    #         "FILE_NAME": "File_Name",
    #         "NUMBER_ELEMENTS": [0, 0, 0],
    #         "CHUNK_SIZE": 0,
    #         "MIN_DATA_VALUE": 0,
    #         "MAX_DATA_VALUE": 0,
    #         "NUMBER_APPEND": [0, 0, 0],
    #         "MODIFY_FIRST_HALF": True,
    #         "MODIFY_SECOND_HALF": False
    #     }
    #     with open("1.yaml", "w") as f:
    #         yaml.safe_dump(data, f, sort_keys=False)
    run("1", 5)
    run("2", 5)
    run("3", 5)
    run("4", 5)
    run("5", 5)
    run("6", 5)
