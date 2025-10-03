from app.auto_clicker_random_delay import AutoClicker

def run_app():
    clicker = AutoClicker()
    clicker.process_user_request()


if __name__ == "__main__":
    run_app()



# #
# # Entry point of the application.
# # It initializes the main controller and starts the automation loop.
# from app.mouse_automation.controller.main_controller import MainController
# if __name__ == "__main__":
#     controller = MainController()
#     controller.run()
