find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_OUR_MODEM gnuradio-our_modem)

FIND_PATH(
    GR_OUR_MODEM_INCLUDE_DIRS
    NAMES gnuradio/our_modem/api.h
    HINTS $ENV{OUR_MODEM_DIR}/include
        ${PC_OUR_MODEM_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_OUR_MODEM_LIBRARIES
    NAMES gnuradio-our_modem
    HINTS $ENV{OUR_MODEM_DIR}/lib
        ${PC_OUR_MODEM_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-our_modemTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_OUR_MODEM DEFAULT_MSG GR_OUR_MODEM_LIBRARIES GR_OUR_MODEM_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_OUR_MODEM_LIBRARIES GR_OUR_MODEM_INCLUDE_DIRS)
