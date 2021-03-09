CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

## ===========================================================================
##  Project Information
## ===========================================================================
PROJECT ( extrafont )
## Package version information.
SET ( PKG_NAME          ${PROJECT_NAME} )
SET ( PKG_MAJOR_VERSION 0 )
SET ( PKG_MINOR_VERSION 6 )
SET ( PKG_BUILD_VERSION 0 )
SET ( PKG_VERSION "${PKG_MAJOR_VERSION}.${PKG_MINOR_VERSION}" )
SET ( PKG_NAME_VERSION  ${PKG_NAME}-${PKG_VERSION} )
SET ( PKG_VENDOR        "RedFantom" )
SET ( PKG_HOME_DIR      ${PROJECT_SOURCE_DIR} )
SET ( PKG_TARGET_LIB_NAME ${PKG_NAME} )

SET ( NO_MSVCRT            ON  )
SET ( VERBOSE              ON  )
SET ( ENABLE_EXPORTS       ON  )

SET ( PKG_SOURCES src/extrafont.c)

MESSAGE ( STATUS "===========================================================" )
MESSAGE ( STATUS " Welcome to the ${PKG_NAME} ${PKG_VERSION} build system!" )
MESSAGE ( STATUS "  * Selected generator:  ${CMAKE_GENERATOR}" )
MESSAGE ( STATUS "  * Operating System ID: "
        ${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_VERSION}-${CMAKE_SYSTEM_PROCESSOR} )
MESSAGE ( STATUS "  * Installation Directory: " ${CMAKE_INSTALL_PREFIX} )
MESSAGE ( STATUS "===========================================================" )

## ===========================================================================
##  Locate Tcl/Tk
## ===========================================================================
MESSAGE(STATUS "Searching for Tcl/Tk...")
FIND_PACKAGE(TCL REQUIRED)
FIND_PACKAGE(TclStub REQUIRED)
MESSAGE(STATUS "  TCL_TCLSH:               " ${TCL_TCLSH})
MESSAGE(STATUS "  TCL_INCLUDE_PATH:        " ${TCL_INCLUDE_PATH})
MESSAGE(STATUS "  TCL_STUB_LIBRARY:        " ${TCL_STUB_LIBRARY})
MESSAGE(STATUS "  TCL_LIBRARY:             " ${TCL_LIBRARY})
MESSAGE(STATUS "  TK_WISH:                 " ${TK_WISH})
MESSAGE(STATUS "  TK_INCLUDE_PATH:         " ${TK_INCLUDE_PATH})
MESSAGE(STATUS "  TK_STUB_LIBRARY:         " ${TK_STUB_LIBRARY})
MESSAGE(STATUS "  TTK_STUB_LIBRARY:        " ${TTK_STUB_LIBRARY})
MESSAGE(STATUS "  TK_LIBRARY:              " ${TK_LIBRARY})
# STRING  ( REPLACE stub "" TCL_LIBRARY_STATIC   ${TCL_STUB_LIBRARY} )
# STRING  ( REPLACE stub "" TK_LIBRARY_STATIC    ${TK_STUB_LIBRARY} )
# MESSAGE ( STATUS "  TCL_LIBRARY_STATIC:      " ${TCL_LIBRARY_STATIC} )
# MESSAGE ( STATUS "  TK_LIBRARY_STATIC:       " ${TK_LIBRARY_STATIC} )

IF ( WIN32 AND NO_MSVCRT )
    STRING ( REPLACE /MD  /MT  CMAKE_C_FLAGS_RELEASE   ${CMAKE_C_FLAGS_RELEASE} )
    STRING ( REPLACE /MDd /MTd CMAKE_C_FLAGS_DEBUG     ${CMAKE_C_FLAGS_DEBUG} )
    STRING ( REPLACE /MD  /MT  CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
    STRING ( REPLACE /MDd /MTd CMAKE_CXX_FLAGS_DEBUG   ${CMAKE_CXX_FLAGS_DEBUG} )
    # SET (    CMAKE_EXE_LINKER_FLAGS
    #       "${CMAKE_EXE_LINKER_FLAGS} /nodefaultlib:MSVCRT.LIB" )
    SET (    CMAKE_EXE_LINKER_FLAGS_RELEASE
            "${CMAKE_EXE_LINKER_FLAGS_RELEASE} LIBCMT.LIB" )
    SET (    CMAKE_EXE_LINKER_FLAGS_DEBUG
            "${CMAKE_EXE_LINKER_FLAGS_DEBUG} LIBCMTD.LIB" )
    # SET (    CMAKE_SHARED_LINKER_FLAGS
    #       "${CMAKE_SHARED_LINKER_FLAGS} /nodefaultlib:MSVCRT.LIB" )
    SET (    CMAKE_SHARED_LINKER_FLAGS_RELEASE
            "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} LIBCMT.LIB" )
    SET (    CMAKE_SHARED_LINKER_FLAGS_DEBUG
            "${CMAKE_SHARED_LINKER_FLAGS_DEBUG}
         /nodefaultlib:LIBCMT.LIB LIBCMTD.LIB" )
    ADD_DEFINITIONS ( -D_STATIC_CPPLIB )
    ADD_DEFINITIONS ( -D_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1 )
    ADD_DEFINITIONS ( -D_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES_COUNT=1 )
ENDIF ( WIN32 AND NO_MSVCRT )

IF ( WIN32 )
    ADD_DEFINITIONS ( -DWIN32 )
    ADD_DEFINITIONS ( -D_WIN32 )
    ADD_DEFINITIONS ( -D_WINDOWS )
    ADD_DEFINITIONS ( -D__WIN32__ )
    SET ( CMAKE_SHARED_LIBRARY_PREFIX lib )
ENDIF ( WIN32 )

IF ( CMAKE_BUILD_TYPE STREQUAL Debug )
    ADD_DEFINITIONS   ( -DGTTK_SYNCHRONIZE )
    ADD_DEFINITIONS   ( -DGTTK_VERBOSE_XERROR_HANDLER )
ENDIF ( CMAKE_BUILD_TYPE STREQUAL Debug )
ADD_DEFINITIONS     ( -DGTTK_INSTALL_XERROR_HANDLER )
ADD_DEFINITIONS     ( -DUSE_TCL_STUBS )
ADD_DEFINITIONS     ( -DUSE_TK_STUBS )
ADD_DEFINITIONS     ( -DUSE_TTK_STUBS )
ADD_DEFINITIONS     ( -DPACKAGE_NAME="${PKG_NAME}" )
ADD_DEFINITIONS     ( -DPACKAGE_VERSION="${PKG_VERSION}" )
INCLUDE_DIRECTORIES ( ${TCL_INCLUDE_PATH} )
INCLUDE_DIRECTORIES ( ${TK_INCLUDE_PATH} )
INCLUDE_DIRECTORIES ( ${TK_INCLUDE_PATH}/tk-private/generic/ttk )
IF ( WIN32 )  # Include additional directories for MSYS build
    INCLUDE_DIRECTORIES ( ${TK_INCLUDE_PATH}/tk8.6/tk-private/generic )
    INCLUDE_DIRECTORIES ( ${TK_INCLUDE_PATH}/tk8.6/tk-private/generic/ttk )
    INCLUDE_DIRECTORIES ( ${TK_INCLUDE_PATH}/tk8.6/tk-private/win )
ENDIF ( WIN32 )
INCLUDE_DIRECTORIES ( ${PROJECT_SOURCE_DIR}/generic )

## ===========================================================================
##  Locate fontconfig
## ===========================================================================
FIND_PACKAGE( Fontconfig )
IF ( ${Fontconfig_FOUND} )
    MESSAGE ( STATUS "Found FontConfig with CMake!" )
ELSE ()
    FIND_PACKAGE( PkgConfig REQUIRED )
    pkg_check_modules ( Fontconfig REQUIRED fontconfig )
    MESSAGE ( STATUS "Found Fontconfig with pkg-config!" )
ENDIF()
MESSAGE ( STATUS "  Fontconfig_INCLUDE_DIRS: " ${Fontconfig_INCLUDE_DIRS} )
MESSAGE ( STATUS "  Fontconfig_LIBRARIES:    " ${Fontconfig_LIBRARIES} )

INCLUDE_DIRECTORIES ( ${Fontconfig_INCLUDE_DIRS} )

## ===========================================================================
##  Target: extrafont shared library
## ===========================================================================
MESSAGE ( STATUS "===========================================================" )
MESSAGE ( STATUS "   ++++ Shared Library: ${PKG_TARGET_LIB_NAME} ++++" )
MESSAGE ( STATUS "===========================================================" )
ADD_LIBRARY ( ${PKG_TARGET_LIB_NAME} SHARED ${PKG_SOURCES} )
TARGET_LINK_LIBRARIES ( ${PKG_TARGET_LIB_NAME} ${TCL_STUB_LIBRARY} )
TARGET_LINK_LIBRARIES ( ${PKG_TARGET_LIB_NAME} ${TK_STUB_LIBRARY} )
TARGET_LINK_LIBRARIES( ${PKG_TARGET_LIB_NAME} ${Fontconfig_LIBRARIES} )
IF ( TTK_STUB_LIBRARY )
    TARGET_LINK_LIBRARIES ( ${PKG_TARGET_LIB_NAME} ${TTK_STUB_LIBRARY} )
ENDIF ( TTK_STUB_LIBRARY )
# IF ( TCL_LIBRARY_STATIC )
#   TARGET_LINK_LIBRARIES ( ${PKG_TARGET_LIB_NAME} ${TCL_LIBRARY_STATIC} )
# ENDIF ( TCL_LIBRARY_STATIC )
# IF ( TK_LIBRARY_STATIC )
#   TARGET_LINK_LIBRARIES ( ${PKG_TARGET_LIB_NAME} ${TK_LIBRARY_STATIC} )
# ENDIF ( TK_LIBRARY_STATIC )

INSTALL ( TARGETS ${PKG_TARGET_LIB_NAME}
        RUNTIME DESTINATION ./tkextrafont
        LIBRARY DESTINATION ./tkextrafont
        ARCHIVE DESTINATION ./tkextrafont )
INSTALL ( FILES
            tkextrafont/pkgIndex.tcl
            tkextrafont/extrafont.tcl
            tkextrafont/futmp.tcl
            tkextrafont/fontnameinfo.tcl
        DESTINATION tkextrafont )
