package ifneeded extrafont 1.2  [list apply { dir  {
	package require Tk

	set libfile libextrafont[info sharedlibextension]
	set libfile_abspath [file join [file normalize $dir] $libfile]
	load $libfile_abspath
	
	namespace eval extrafont {}
	source [file join $dir extrafont.tcl]
	source [file join $dir futmp.tcl]
	
	package provide extrafont 1.2

}} $dir] ;# end of lambda apply
