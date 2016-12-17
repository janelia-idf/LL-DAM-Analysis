# explore the wx.calendar.CalendarCtrl() control
2.# allows for point and click date input
3.
4.import wx
5.import wx.calendar as cal
6.
7.class MyCalendar(wx.Dialog):
8.    """create a simple dialog window with a calendar display"""
9.    def __init__(self, parent, mytitle):
10.        wx.Dialog.__init__(self, parent, wx.ID_ANY, mytitle)
11.        # use a box sizer to position controls vertically
12.        vbox = wx.BoxSizer(wx.VERTICAL)
13.
14.        # wx.DateTime_Now() sets calendar to current date
15.        self.calendar = cal.CalendarCtrl(self, wx.ID_ANY, wx.DateTime_Now())
16.        vbox.Add(self.calendar, 0, wx.EXPAND|wx.ALL, border=20)
17.        # click on day
18.        self.calendar.Bind(cal.EVT_CALENDAR_DAY, self.onCalSelected)
19.        # change month
20.        #self.calendar.Bind(cal.EVT_CALENDAR_MONTH, self.onCalSelected)
21.        # change year
22.        #self.calendar.Bind(cal.EVT_CALENDAR_YEAR, self.onCalSelected)
23.
24.        self.label = wx.StaticText(self, wx.ID_ANY, 'click on a day')
25.        vbox.Add(self.label, 0, wx.EXPAND|wx.ALL, border=20)
26.
27.        button = wx.Button(self, wx.ID_ANY, 'Exit')
28.        vbox.Add(button, 0, wx.ALL|wx.ALIGN_CENTER, border=20)
29.        self.Bind(wx.EVT_BUTTON, self.onQuit, button)
30.
31.        self.SetSizerAndFit(vbox)
32.        self.Show(True)
33.        self.Centre()
34.
35.    def onCalSelected(self, event):
36.        #date = event.GetDate()
37.        date = self.calendar.GetDate()
38.        day = date.GetDay()
39.        # for some strange reason month starts with zero
40.        month = date.GetMonth() + 1
41.        # year is yyyy format
42.        year = date.GetYear()
43.        # format the date string to your needs
44.        ds = "%02d/%02d/%d \n" % (month, day, year)
45.        self.label.SetLabel(ds)
46.
47.    def onQuit(self, event):
48.        self.Destroy()
49.
50.
51.app = wx.App(0)
52.MyCalendar(None, 'wx.calendar.CalendarCtrl()')
53.app.MainLoop()
