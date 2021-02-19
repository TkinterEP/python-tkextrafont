package ifneeded extrafont 1.2  [list apply { dir  {
	package require Tk
	
	set thisDir [file normalize ${dir}]

	set os $::tcl_platform(platform)
	switch -- $os {
		windows { set os win }
		unix    {
			switch -- $::tcl_platform(os) {
				Darwin { set os darwin }
				Linux  { set os linux  }
			}
		}
	}
	set libfile libextrafont[info sharedlibextension]
	 # Try to guess the tcl-interpreter architecture (32/64 bit) ...
	set arch $::tcl_platform(pointerSize)
	switch -- $arch {
		4 { set arch x32  }
		8 { set arch x64 }
		default { error "extrafont: Unsupported architecture: Unexpected pointer-size $arch!!! "}
	}
	

	set libfile_abspath [file join [file normalize $dir] $libfile]
	load $libfile_abspath
	
	namespace eval extrafont {}
	source [file join $thisDir extrafont.tcl]
	source [file join $thisDir futmp.tcl]
	
	package provide extrafont 1.2

}} $dir] ;# end of lambda apply
