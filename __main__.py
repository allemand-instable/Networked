from view_splashscreen import View_SplashScreen
from parameters import Parameters
from view_select_action import View_SelectAction
from network_service_interface import NetworkService_Interface

params = Parameters()
network_services = NetworkService_Interface(params)
view = View_SelectAction(params, network_services)
view.run()
