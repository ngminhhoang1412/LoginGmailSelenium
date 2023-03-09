import undetected_chromedriver as uc2


class Driver(uc2.Chrome):
    def __init__(self, quit_callback=None, **kw):
        super().__init__(**kw)
        self.quit_callback = quit_callback

    def quit(self):
        try:
            super().execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})
        except (Exception, ValueError):
            pass
        super().close()
        super().quit()
        try:
            self.quit_callback()
        except (Exception, ValueError):
            pass
