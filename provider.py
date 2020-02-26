import os
import logging
class Provider:
    """
    Класс для провайдера, принимает имя провайдера, массив проверяемых через него IP, 
    и маршрут по умолчанию для данного провайдера
    """

    def __init__(self, name, gatway, test_hosts):
        self.ping_list = [1] * 50
        self.test_hosts = test_hosts
        self.gatway = gatway
        self.set_routes()
        self.last = self.ping_list[-1]
        self.name = name

    def add_value(self, value):
        """
        Удаляет значение потерь из начала массива и добовляет новое в конец, таким
        образом имеется буфер с n последних значений
        """
        del self.ping_list[0]
        self.ping_list.append(value)

    def is_bad(self):
        """
        Возвращает True если провайдер работет нестибильно, иначе False.
        Используется для определения того, что нужно переключится на резерв
        """
        last_nums = 20
        percent = 15
        if sum(self.ping_list[-last_nums:])/last_nums > percent:
            return True
        else:
            return False

    def can_resume(self):
        """
        Возвращает True если провайдер работет стибильно, иначе False.
        Используется для определения того, что нужно переключится на восстановившийся канал
        """
        last_nums = 40
        percent = 5
        max_loss = 25
        if max(self.ping_list[-last_nums:]) > max_loss:
            return False
        elif sum(self.ping_list[-last_nums:])/last_nums > percent:
            return False
        else:
            return True
    
    def is_default(self):
        """Возвращает True если в данный момент маршрут по умолчанию через этого провайдера, иначе False."""
        default_gateway = list(os.popen('ip route '))[0].split()[2]
        if default_gateway == self.gatway:
            return True 
        else:
            return False

    def set_default(self):
        """Устанавливает маршрут по умолчанию через этого провайдера."""
        os.popen('ip route replace default via {}'.format(self.gatway))
        if os.path.exists('/etc/openvpn/'):
            os.popen('/etc/init.d/openvpn restart')
    
    def set_routes(self):
        """Устанавливает маршруты к пингуемым хостам через этого провайдера."""
        for dest in self.test_hosts:
            os.popen('ip route add {}/32 via {}'.format(dest, self.gatway))
      
    def log_status(self, comment):
        """Пишет в лог информацию о состоянии канала и массив с результатами последних проверок с переданным коментарием"""
        logging.warn('{} : {} : is_bad={}, canRezume={}, is_default={}'.format(comment, self.name, self.is_bad(), self.can_resume(), self.is_default()))
        logging.warn('{} : {} : ping_list: {}'.format(comment, self.name, str(self.ping_list)))


