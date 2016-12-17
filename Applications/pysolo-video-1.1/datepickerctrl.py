import wx
import datetime
import wx.lib.masked as masked
import wx.lib.newevent
import os

class mainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.sizers()

    def onDateTimeChanged(self, event):
        date1 = self.start_date.GetValue()
        date2 = datetime.date(*map(int, date1.FormatISODate().split('-')))
#        date2 = date1.date()
        time1 = self.start_time.GetValue(self)
        time2 = datetime.time(*map(int, time1.FormatISOTime().split(':')))
#        time2 = datetime.datetime.time(time1)
#        time2 = datetime.time(1,1,1)
        print("$$$$$$ pvg_panel_one; 593; start date = ", date1)
        print("$$$$$$ pvg_panel_one; start time = ", time1)
        self.start_datetime = datetime.datetime.combine(date2, time2)
        print("$$$$$$ pvg_panel_one; start time = ", self.start_datetime)

    def sizers(self):
        sb_datetime = wx.StaticBox(self, -1, "Video Start Date and Time")
        self.date_time_sizer = wx.StaticBoxSizer(sb_datetime, wx.HORIZONTAL)

        self.txt_date = wx.StaticText(self, -1, "Date:")
        self.start_date = wx.DatePickerCtrl(self, wx.ID_ANY, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

        self.Bind(wx.EVT_DATE_CHANGED, self.onDateTimeChanged, self.start_date)  # $$$$$$ - set default date to start_datetime

        self.date_time_sizer.Add(self.txt_date, 0, wx.ALL, 5)  # --- add to datetime row, center panel, lower sizer
        self.date_time_sizer.Add(self.start_date, 0, wx.ALL, 5)

        # ---------------------------------------------------------------------  time picker
        self.txt_time = wx.StaticText(self, -1, "Time (24-hour format):")
        self.spinbtn = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, 20), wx.SP_VERTICAL)
        self.start_time = masked.TimeCtrl(self, -1, name="24 hour control", fmt24hr=True, spinButton=self.spinbtn)
        self.Bind(masked.EVT_TIMEUPDATE, self.onDateTimeChanged, self.start_time)  # $$$$$$ - set default date to start_datetime

        self.date_time_sizer.Add(self.txt_time)
        self.date_time_sizer.Add(self.start_time)
        self.date_time_sizer.Add(self.spinbtn)


        self.SetSizer(self.date_time_sizer)

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.
