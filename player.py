#!/usr/bin/env python -tt
"""
A simple player frame for listening feiyuxiu

Based on wxPython and VLC

Author: Ran Zhou
Date: 07-21-2012
"""


import wx
import vlc
import cal
import url
from datetime import date


class Player(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, pos=wx.DefaultPosition, size=(520, 300))
        #Menu Bar
        self.frame_menubar = wx.MenuBar()

        #Play Menu
        self.file_menu = wx.Menu()
        #Quit item
        quit_item = self.file_menu.Append(2, '&Quit\tCTRL+Q', "Quit the app")
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)

        #Append Play to Menu Bar
        self.frame_menubar.Append(self.file_menu, "&Play")
        self.SetMenuBar(self.frame_menubar)

        #Choice panel
        self.choice_panel = wx.Panel(self, -1)

        #Date box
        dates = cal.default_dates()
        day_choices = cal.date_str(dates)
        date_box = wx.ComboBox(self.choice_panel, value=day_choices[-1], pos=(5, 0), choices=day_choices, style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect, date_box)

        #Custom date
        wx.StaticText(self.choice_panel, pos=(287, 2), label='Y')
        self.custom_year = wx.TextCtrl(self.choice_panel, pos=(305, 0), size=(40, -1))
        self.custom_year.AppendText(str(dates[-1].year))
        wx.StaticText(self.choice_panel, pos=(353, 2), label='M')
        self.custom_month = wx.TextCtrl(self.choice_panel, pos=(370, 0), size=(20, -1))
        self.custom_month.AppendText(str(dates[-1].month))
        wx.StaticText(self.choice_panel, pos=(395, 2), label='D')
        self.custom_day = wx.TextCtrl(self.choice_panel, pos=(410, 0), size=(20, -1))
        self.custom_day.AppendText(str(dates[-1].day))
        choose = wx.Button(self.choice_panel, pos=(450, 0), label='Set', size=(50, -1))
        self.Bind(wx.EVT_BUTTON, self.SetCustom, choose)

        #Control panel
        self.ctrlpanel = wx.Panel(self, -1)
        self.timeslider = wx.Slider(self.ctrlpanel, -1, 0, 0, 1000, pos=(5, 60), size=(500, -1))
        self.timeslider.SetRange(0, 1000)
        play        = wx.Button(self.ctrlpanel, label="Play", pos=(5, 0), size=(50, -1))
        pause       = wx.Button(self.ctrlpanel, label="Pause", pos=(55, 0), size=(60, -1))
        stop        = wx.Button(self.ctrlpanel, label="Stop", pos=(115, 0), size=(50, -1))
        next_item   = wx.Button(self.ctrlpanel, label="Next", pos=(5, 30), size=(50, -1))
        previous_item = wx.Button(self.ctrlpanel, label="Prev", pos=(55, 30), size=(50, -1))
        volume      = wx.Button(self.ctrlpanel, label="Mute", pos=(450, 0), size=(50, -1))
        self.volslider = wx.Slider(self.ctrlpanel, -1, 0, 0, 100, pos=(340, 0), size=(100, -1))
#
#        # Bind controls to events
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        self.Bind(wx.EVT_BUTTON, self.OnStop, stop)
        self.Bind(wx.EVT_BUTTON, self.OnNext, next_item)
        self.Bind(wx.EVT_BUTTON, self.OnPrevious, previous_item)
        self.Bind(wx.EVT_BUTTON, self.OnToggleVolume, volume)
        self.Bind(wx.EVT_SLIDER, self.OnSetVolume, self.volslider)

        #Info panel
        self.info_panel = wx.Panel(self, -1)
        self.info_panel.SetBackgroundColour(wx.LIGHT_GREY)

        #Infomation to display
        self.info_line1 = wx.StaticLine(self.info_panel, pos=(5, 5))
        self.info_title = wx.StaticText(self.info_panel, pos=(5, 10), label='Easy Morning Fei Yu Xiu @ CRI Radio:')
        self.info_playing = wx.StaticText(self.info_panel, pos=(5, 40), label='')

        #Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info_panel, 1, flag=wx.EXPAND)
        sizer.Add(self.choice_panel, flag=wx.EXPAND | wx.TOP, border=10)
        sizer.Add(self.ctrlpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=15)
        self.SetSizer(sizer)
        self.SetMinSize((520, 300))

        # finally create the timer, which updates the timeslider
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.playerl = self.Instance.media_list_player_new()
#        self.toolbar = self.CreateToolBar()
#        self.player_latest_tool = self.toolbar.AddLabelTool(wx.ID_)

    def OnQuit(self, evt):
        self.Close()

    def OnSelect(self, evt):
        day = evt.GetString()
        dat = cal.str_date(day)
        if_exist = url.res_exist(dat)
        self.NoRes(if_exist)
        mms_urls = url.mms_url(dat)
        self.info_playing.SetLabel(day + '  ' + url.mms_sect(mms_urls[0]))
        self.OnStop(None)
        self.Media_list = self.Instance.media_list_new()
        for mms in mms_urls:
            self.Media_list.add_media(self.Instance.media_new_location(mms))
        self.playerl.set_media_list(self.Media_list)
        self.playerl.set_media_player(self.player)
        if self.playerl.play() == -1:
            self.errorDialog('Unable to play.')
        else:
            self.timer.Start(1,)
        self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def OnPlay(self, evt):
        """Toggle the status to Play/Pause.

        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # wx.FileDialog to select a file
        if not self.player.get_media():
            self.SetCustom()
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")
            else:
                self.timer.Start()

    def OnNext(self, evt):
        self.playerl.next()

    def OnPrevious(self, evt):
        self.playerl.previous()

    def OnPause(self, evt):
        """Pause the player.
        """
        self.player.pause()

    def OnStop(self, evt):
        """Stop the player.
        """
        self.player.stop()
        self.playerl.stop()
        # reset the time slider
        self.timeslider.SetValue(0)
        self.timer.Stop()

    def OnTimer(self, evt):
        """Update the time slider according to the current movie time.
        """
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        self.timeslider.SetRange(-1, length)

        # update the time on the slider
        time = self.player.get_time()
        self.timeslider.SetValue(time)

    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def OnSetVolume(self, evt):
        """Set the volume according to the volume sider.
        """
        volume = self.volslider.GetValue() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK | wx.ICON_ERROR)
        edialog.ShowModal()

    def SetCustom(self, evt):
        year = self.custom_year.GetValue()
        month = self.custom_month.GetValue()
        day = self.custom_day.GetValue()
        string = '%-4s-%2s-%-2s' % (year, month, day)
        dat = cal.str_date(string)
        if_exist = url.res_exist(dat)
        self.NoRes(if_exist)
        mms_urls = url.mms_url(dat)
        self.info_playing.SetLabel(string + '  ' + url.mms_sect(mms_urls[0]))

        self.OnStop(None)
        self.Media_list = self.Instance.media_list_new()
        for mms in mms_urls:
            self.Media_list.add_media(self.Instance.media_new_location(mms))
        self.playerl.set_media_list(self.Media_list)
        self.playerl.set_media_player(self.player)
        if self.playerl.play() == -1:
            self.errorDialog('Unable to play.')
        else:
            self.timer.Start(1,)
        self.volslider.SetValue(self.player.audio_get_volume() / 2)

    def NoRes(self, if_exist):
        if not if_exist:
            self.errorDialog('Resource may not exist')


def main():
    app = wx.App()
    player = Player('A Simple FeiYuXiu Player')
    player.Center()
    player.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
