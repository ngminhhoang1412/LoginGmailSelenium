import undetected_chromedriver as uc2


class Driver(uc2.Chrome):
    def __init__(self, quit_callback=None, **kw):
        super().__init__(**kw)
        self.quit_callback = quit_callback

    def quit(self):
        callback_executed = False
        try:
            super().execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})
            super().close()
            super().quit()
            callback_executed = True
            self.quit_callback()
        except (Exception, ValueError):
            if callback_executed:
                print('Error executing quit callback')
            else:
                print('Error quitting driver')
