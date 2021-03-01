#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Audiobook Metadata Panel for all tags.
"""

import wx

import ivonet
from ivonet.book.meta import GENRES, CHAPTER_LIST
from ivonet.events import ee, log, _
from ivonet.gui.CoverArtStaticBitmap import CoverArtStaticBitmap

try:
    # The images.py file is generated by images.sh in the root of the project
    from ivonet.image.images import yoda
except ImportError:
    raise ImportError("The images file was not found. Did you forget to generate them?")


def handle_numeric_keypress(event):
    keycode = event.GetKeyCode()
    if keycode < 255 and chr(keycode).isnumeric():
        event.Skip()


class AudiobookMetaDataPanel(wx.Panel):
    """The panel to the left of the M4B where the audiobook metadata can be edited."""

    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.project = None

        hs_left_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        fgs_lft_pnl_m4b_page = wx.FlexGridSizer(3, 1, 4, 0)
        hs_left_pnl_m4b_page.Add(fgs_lft_pnl_m4b_page, 1, wx.ALL | wx.EXPAND, 0)

        fgs_mp3_metadata = wx.FlexGridSizer(6, 2, 4, 16)
        fgs_lft_pnl_m4b_page.Add(fgs_mp3_metadata, 1, wx.EXPAND, 0)

        lbl_title = wx.StaticText(self, wx.ID_ANY, "Title")
        fgs_mp3_metadata.Add(lbl_title, 1, 0, 0)

        self.tc_title = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_title.SetToolTip("Title of the book")
        fgs_mp3_metadata.Add(self.tc_title, 0, wx.EXPAND, 0)

        lbl_artist = wx.StaticText(self, wx.ID_ANY, "Artist")
        fgs_mp3_metadata.Add(lbl_artist, 0, wx.EXPAND, 0)

        self.tc_artist = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_artist.SetToolTip("The author or album artist")
        fgs_mp3_metadata.Add(self.tc_artist, 0, wx.EXPAND, 0)

        lbl_grouping = wx.StaticText(self, wx.ID_ANY, "Grouping")
        fgs_mp3_metadata.Add(lbl_grouping, 1, 0, 0)

        self.tc_grouping = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_grouping.SetToolTip("Grouping e.g. series")
        fgs_mp3_metadata.Add(self.tc_grouping, 0, wx.EXPAND, 0)

        lbl_genre = wx.StaticText(self, wx.ID_ANY, "Genre")
        fgs_mp3_metadata.Add(lbl_genre, 0, 0, 0)

        self.cb_genre = wx.ComboBox(self, wx.ID_ANY,
                                    choices=GENRES,
                                    style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_genre.SetToolTip("Select your genre")
        self.cb_genre.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_genre, 0, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

        label_1 = wx.StaticText(self, wx.ID_ANY, "Chapter text")
        fgs_mp3_metadata.Add(label_1, 0, 0, 0)

        self.tc_chapter_text = wx.TextCtrl(self, wx.ID_ANY, "Chapter")
        self.tc_chapter_text.SetToolTip("Text to use fore chapterisation")
        fgs_mp3_metadata.Add(self.tc_chapter_text, 0, wx.EXPAND, 0)

        lbl_chapterisation = wx.StaticText(self, wx.ID_ANY, "Chapters")
        fgs_mp3_metadata.Add(lbl_chapterisation, 1, 0, 0)

        self.cb_chapterisation = wx.ComboBox(self, wx.ID_ANY,
                                             choices=CHAPTER_LIST,
                                             style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.cb_chapterisation.SetToolTip("Choose which chapterisation method is preferred")
        self.cb_chapterisation.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_chapterisation, 0, wx.EXPAND, 0)

        vs_mp3_metadata_1 = wx.BoxSizer(wx.VERTICAL)
        fgs_lft_pnl_m4b_page.Add(vs_mp3_metadata_1, 1, wx.EXPAND, 0)

        vs_track_year_comment = wx.BoxSizer(wx.VERTICAL)
        vs_mp3_metadata_1.Add(vs_track_year_comment, 1, wx.EXPAND, 0)

        hs_track_year = wx.BoxSizer(wx.HORIZONTAL)
        vs_track_year_comment.Add(hs_track_year, 0, wx.ALL | wx.EXPAND, 0)

        hs_track_year = wx.BoxSizer(wx.HORIZONTAL)
        vs_track_year_comment.Add(hs_track_year, 0, wx.ALL | wx.EXPAND, 0)

        lbl_disc = wx.StaticText(self, wx.ID_ANY, "Disc")
        hs_track_year.Add(lbl_disc, 0, 0, 0)

        hs_track_year.Add((60, 20), 0, 0, 0)

        self.sc_disc = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        self.sc_disc.SetToolTip("which disk?")
        hs_track_year.Add(self.sc_disc, 0, 0, 0)

        label_8 = wx.StaticText(self, wx.ID_ANY, "of")
        hs_track_year.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sc_disk_total = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        self.sc_disk_total.SetToolTip("Total number of discs for this book")
        hs_track_year.Add(self.sc_disk_total, 0, 0, 0)

        hs_track_year.Add((32, 20), 0, 0, 0)

        lbl_year = wx.StaticText(self, wx.ID_ANY, "Year")
        hs_track_year.Add(lbl_year, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.tc_year = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_year.Bind(wx.EVT_CHAR, handle_numeric_keypress)

        self.tc_year.SetToolTip("Publication year")
        hs_track_year.Add(self.tc_year, 1, wx.EXPAND, 0)

        vs_comment = wx.BoxSizer(wx.VERTICAL)
        vs_track_year_comment.Add(vs_comment, 0, wx.EXPAND, 0)

        vs_comment_1 = wx.BoxSizer(wx.VERTICAL)
        vs_comment.Add(vs_comment_1, 2, wx.ALL | wx.EXPAND, 0)

        lbl_comment = wx.StaticText(self, wx.ID_ANY, "Comment")
        vs_comment_1.Add(lbl_comment, 0, wx.LEFT, 0)

        self.tc_comment = wx.TextCtrl(self, wx.ID_ANY, ivonet.TXT_COMMENT, style=wx.TE_MULTILINE)
        self.tc_comment.SetToolTip("Add your comments here")
        vs_comment_1.Add(self.tc_comment, 2, wx.EXPAND, 0)

        vs_mp3_metadata_2 = wx.BoxSizer(wx.VERTICAL)
        fgs_lft_pnl_m4b_page.Add(vs_mp3_metadata_2, 1, wx.EXPAND, 0)

        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        vs_mp3_metadata_2.Add(sizer_17, 1, wx.ALL | wx.EXPAND, 0)

        label_11 = wx.StaticText(self, wx.ID_ANY, "Cover art")
        sizer_17.Add(label_11, 0, 0, 0)

        self.pnl_cover_art = wx.Panel(self, wx.ID_ANY)

        sizer_17.Add(self.pnl_cover_art, 1, wx.ALL | wx.EXPAND, 0)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.cover_art = CoverArtStaticBitmap(self.pnl_cover_art)
        sizer_1.Add(self.cover_art, 1, wx.EXPAND, 0)

        self.pnl_cover_art.SetSizer(sizer_1)

        fgs_mp3_metadata.AddGrowableCol(1)

        fgs_lft_pnl_m4b_page.AddGrowableRow(2)

        self.SetSizer(hs_left_pnl_m4b_page)

        self.Layout()

        # Bind the field events to methods
        self.Bind(wx.EVT_TEXT, self.on_title, self.tc_title)
        self.Bind(wx.EVT_TEXT, self.on_artist, self.tc_artist)
        self.Bind(wx.EVT_TEXT, self.on_grouping, self.tc_grouping)
        self.Bind(wx.EVT_COMBOBOX, self.on_genre, self.cb_genre)
        self.Bind(wx.EVT_TEXT, self.on_chapter_text, self.tc_chapter_text)
        self.Bind(wx.EVT_COMBOBOX, self.on_chapter_method, self.cb_chapterisation)
        self.Bind(wx.EVT_SPINCTRL, self.on_disc, self.sc_disc)
        self.Bind(wx.EVT_SPINCTRL, self.on_disc, self.sc_disk_total)
        self.Bind(wx.EVT_TEXT, self.on_year, self.tc_year)
        self.Bind(wx.EVT_TEXT, self.on_comment, self.tc_comment)

        # bind the ee events to methods
        ee.on("project.new", self.ee_reset_metadata)
        ee.on("project.cover_art", self.ee_project_cover_art)
        ee.on("project.tracks", self.ee_tracks_changed)

        ee.on("track.title", self.ee_on_title)
        ee.on("track.album", self.ee_on_title)
        ee.on("track.artist", self.ee_on_artist)
        ee.on("track.disc", self.ee_on_disc)
        ee.on("track.disc_total", self.ee_on_disc_total)
        ee.on("track.genre", self.ee_on_genre)
        ee.on("track.comment", self.ee_on_comment)
        ee.on("track.year", self.ee_on_year)
        # ee.on("track.mp3", self.ee_on_mp3)

        # 'dirty' flags
        self.genre_pristine = True

    def ee_reset_metadata(self, project):
        """Handles the 'audiobook.new' event to reset the whole space"""
        _("ee_reset_metadata", project)
        self.project = project
        self.genre_pristine = True
        if not project.has_cover_art():
            self.cover_art.reset()
        self.tc_title.SetValue(project.title)
        self.tc_artist.SetValue(project.artist)
        self.tc_grouping.SetValue(project.grouping)
        self.cb_genre.SetValue(project.genre)
        self.tc_chapter_text.SetValue(project.chapter_text)
        self.cb_chapterisation.SetSelection(project.chapter_method)
        self.sc_disc.SetValue(project.disc)
        self.sc_disk_total.SetValue(project.disc_total)
        self.tc_year.SetValue(project.year)
        self.tc_comment.SetValue(project.comment)

    def ee_tracks_changed(self, tracks):
        """Handles the 'track.mp3' event to reset the whole space"""
        self.project.tracks = tracks

    def ee_project_cover_art(self, image):
        _("Adding Cover Art to project")
        self.project.cover_art = image

    def on_title(self, event):
        """Handler for the title field event"""
        self.project.title = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def ee_on_title(self, value):
        """Handler for the 'track.title' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.tc_title.IsEmpty():
            self.tc_title.SetValue(value)

    def on_artist(self, event):
        """Handler for the artist field event"""
        self.project.artist = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def ee_on_artist(self, value):
        """Handler for the 'track.artist' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.tc_artist.IsEmpty():
            self.tc_artist.SetValue(value)

    def on_grouping(self, event):
        """Handler for the grouping field event"""
        self.project.grouping = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def ee_on_grouping(self, value):
        """Handler for the 'track.grouping' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.tc_grouping.IsEmpty():
            self.tc_grouping.SetValue(value)

    def on_genre(self, event):
        """Handler for the genre field event"""
        self.project.genre = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def ee_on_genre(self, value):
        """Handler for the 'track.title' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        In this case we need a 'dirty' flag to do this as the field is a drop down and is never empty
        This event is less important then manual or previous set values.
        """
        if self.genre_pristine:
            if value in GENRES:
                self.genre_pristine = False
                self.cb_genre.SetValue(value)
            else:
                log(f"Genre {value} from the metadata is not a known genre.")

    def on_chapter_text(self, event):
        """Handler for the chapter text field event"""
        self.project.chapter_text = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def on_chapter_method(self, event):
        """Handler for the chapter convert method field event"""
        self.project.chapter_method = event.GetString()
        _(event.GetString())
        event.StopPropagation()

    def on_disc(self, event):
        """Handler for the disc and disc_total field events as they are linked"""
        self.check_disc()
        self.project.disc = self.sc_disc.GetValue()
        self.project.disc_total = self.sc_disk_total.GetValue()
        _(self.project)
        event.StopPropagation()

    def ee_on_disc(self, value):
        """Handler for the 'track.disc' event.
        It will always set it and that will trigger the on_disc handler
        to check if all is well...
        """
        self.sc_disc.SetValue(int(value))

    def ee_on_disc_total(self, value):
        """Handler for the 'track.disc_total' event.
        It will always set it and that will trigger the on_disc handler
        to check if all is well...
        """
        self.sc_disk_total.SetValue(int(value))

    def on_year(self, event):
        """Handler for the year field event"""
        self.project.year = event.GetString()
        event.StopPropagation()

    def ee_on_year(self, value):
        """Handler for the 'track.year' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.tc_year.IsEmpty():
            self.tc_year.SetValue(value)

    def on_comment(self, event):
        """Handler for the comment field event"""
        self.project.comment = event.GetString()
        event.StopPropagation()

    def ee_on_comment(self, value):
        """Handler for the 'track.comment' event.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.tc_comment.IsEmpty() or self.tc_comment.GetValue() == ivonet.TXT_COMMENT:
            self.tc_comment.SetValue(value)

    def check_disc(self):
        if self.sc_disk_total.GetValue() < self.sc_disc.GetValue():
            log("Correcting disk total as it can not be smaller than the disk.")
            self.sc_disk_total.SetValue(self.sc_disc.GetValue())
