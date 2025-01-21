import cloudkube.clusterConfig as clusterConfig
from .ClusterManager import ClusterManager
from .displayUtils import printb


def display_welcome_message():
    logo = """
 ____  _     ____  _     ____  _  __ _     ____  _____
/   _\/ \   /  _ \/ \ /\/  _ \/ |/ // \ /\/  _ \/  __/
|  /  | |   | / \|| | ||| | \||   / | | ||| | //|  \  
|  \_ | |_/\| \_/|| \_/|| |_/||   \ | \_/|| |_\\|  /_ 
\____/\____/\____/\____/\____/\_|\_\\____/\____/\____\                                                    
    """
    print("========================================================")
    print(logo)
    print("========================================================")


def display_menu_options():
    print()
    printb("Please select from the following menu options:")
    print("1. Configure cloud credentials.")
    print("2. Configure cluster configuration.")
    print("3. Spin up cluster.")
    print("4. Tear down cluster.")
    print("5. Exit")
    print()


def run_wizard():
    while True:
        display_menu_options()
        selection = input("Selection: ")
        print()
        match selection:
            case "1":
                print("ERROR: This has not yet been implemented. TODO!")
            case "2":
                clusterConfig.configure_cluster_interactive()
            case "3":
                ClusterManager.spin_up_cluster()
            case "4":
                ClusterManager.tear_down_cluster()
            case "5":
                print("exiting...")
                break
            case _:
                print("Invalid option selected. Please re-enter.")


def main():
    display_welcome_message()
    run_wizard()


# if __name__ == "__main__":
#     display_welcome_message()
#     run_wizard()
