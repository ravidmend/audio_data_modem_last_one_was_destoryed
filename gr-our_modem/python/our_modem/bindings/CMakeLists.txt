# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT our_modem_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT our_modem_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND our_modem_python_files python_bindings.cc)

gr_pybind_make_oot(our_modem ../../.. gr::our_modem "${our_modem_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET our_modem_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:our_modem_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/our_modem/)

install(
    TARGETS our_modem_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/our_modem
    COMPONENT pythonapi)
