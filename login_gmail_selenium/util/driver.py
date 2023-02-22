import undetected_chromedriver as uc2


class Driver(uc2.Chrome):
    def __init__(self, quit_callback=None, **kw):
        super().__init__(**kw)
        self.quit_callback = quit_callback

    def quit(self):
        self.execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})
        self.close()
        super().quit()
        self.quit_callback()
