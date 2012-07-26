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

        #Playback Menu
        self.file_menu = wx.Menu()
        #Quit item
        play_item = self.file_menu.Append(1, '&Play\tCTRL+P', "Play")
        self.Bind(wx.EVT_MENU, self.OnPlay, play_item)
        stop_item = self.file_menu.Append(2, '&Stop\tCTRL+S', "Stop")
        self.Bind(wx.EVT_MENU, self.OnStop, stop_item)
        prev_item = self.file_menu.Append(3, '&Previous\tCTRL+B', "Previous")
        self.Bind(wx.EVT_MENU, self.OnPrevious, prev_item)
        next_item = self.file_menu.Append(4, '&Next\tCTRL+N', "Next")
        self.Bind(wx.EVT_MENU, self.OnNext, next_item)
        quit_item = self.file_menu.Append(5, '&Quit\tCTRL+Q', "Quit the app")
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)

        #Append Play to Menu Bar
        self.frame_menubar.Append(self.file_menu, "&Playback")
        self.SetMenuBar(self.frame_menubar)

        #Audio Menu
        self.audio_menu = wx.Menu()
        mute_item = self.audio_menu.Append(1, 'Mute\tCTRL+M', "Mute")
        self.Bind(wx.EVT_MENU, self.OnToggleVolume, mute_item)
        #Append Play to Menu Bar
        self.frame_menubar.Append(self.audio_menu, "&Audio")
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
        choose = wx.Button(self.choice_panel, pos=(445, 0), label='Choose', size=(65, -1))
        self.Bind(wx.EVT_BUTTON, self.SetCustom, choose)

        #Control panel
        self.ctrlpanel = wx.Panel(self, -1)
        self.timeslider = wx.Slider(self.ctrlpanel, -1, 0, 0, 1000, pos=(5, 50), size=(500, -1))
        self.timeslider.SetRange(0, 1000)

        #Image
        play_img    = wx.Image('./button/play.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        pause_img   = wx.Image('./button/pause.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        stop_img    = wx.Image('./button/stop.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        next_img    = wx.Image('./button/next.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        prev_img    = wx.Image('./button/previous.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        vol_img    = wx.Image('./button/sound_high.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        play        = wx.BitmapButton(self.ctrlpanel, bitmap=play_img, pos=(5, 0))
        pause       = wx.BitmapButton(self.ctrlpanel, bitmap=pause_img, pos=(50, 0))
        stop        = wx.BitmapButton(self.ctrlpanel, bitmap=stop_img, pos=(95, 0))
        next_item   = wx.BitmapButton(self.ctrlpanel, bitmap=next_img, pos=(140, 0))
        previous_item   = wx.BitmapButton(self.ctrlpanel, bitmap=prev_img, pos=(185, 0))
        volume   = wx.BitmapButton(self.ctrlpanel, bitmap=vol_img, pos=(455, 0))
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
        sizer.Add(self.ctrlpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
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
        self.d_string = day
        dat = cal.str_date(day)
        if_exist = url.res_exist(dat)
        self.NoRes(if_exist)
        self.i = 0
        self.mms_urls = url.mms_url(dat)
        self.info_playing.SetLabel(self.d_string + '  ' + url.mms_sect(self.mms_urls[self.i]))
        self.OnStop(None)
        self.Media_list = self.Instance.media_list_new()
        for mms in self.mms_urls:
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
            self.SetCustom(evt)
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")
            else:
                self.timer.Start()

    def OnNext(self, evt):
        self.i += 1
        self.info_playing.SetLabel(self.d_string + '  ' + url.mms_sect(self.mms_urls[self.i]))
        self.playerl.next()

    def OnPrevious(self, evt):
        self.i -= 1
        self.info_playing.SetLabel(self.d_string + '  ' + url.mms_sect(self.mms_urls[self.i]))
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
        self.d_string = '%-4s-%2s-%-2s' % (year, month, day)
        dat = cal.str_date(self.d_string)
        if_exist = url.res_exist(dat)
        self.NoRes(if_exist)
        self.i = 0
        self.mms_urls = url.mms_url(dat)
        self.info_playing.SetLabel(self.d_string + '  ' + url.mms_sect(self.mms_urls[self.i]))

        self.OnStop(None)
        self.Media_list = self.Instance.media_list_new()
        for mms in self.mms_urls:
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
