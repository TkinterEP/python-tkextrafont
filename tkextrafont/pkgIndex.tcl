package ifneeded extrafont 1.2 \
    "pwd;
     source extrafont.tcl; \
     source futmp.tcl; \
     load [file join [list [pwd]] libextrafont[info sharedlibextension]];
     package provide extrafont 1.2;"
