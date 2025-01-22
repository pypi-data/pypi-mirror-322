#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "xronos::_runtime" for configuration "Release"
set_property(TARGET xronos::_runtime APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(xronos::_runtime PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELEASE ""
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/xronos/_runtime.cpython-313-aarch64-linux-gnu.so"
  IMPORTED_NO_SONAME_RELEASE "TRUE"
  )

list(APPEND _IMPORT_CHECK_TARGETS xronos::_runtime )
list(APPEND _IMPORT_CHECK_FILES_FOR_xronos::_runtime "${_IMPORT_PREFIX}/xronos/_runtime.cpython-313-aarch64-linux-gnu.so" )

# Import target "xronos::runtime" for configuration "Release"
set_property(TARGET xronos::runtime APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(xronos::runtime PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/xronos/libruntime.so"
  IMPORTED_SONAME_RELEASE "libruntime.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS xronos::runtime )
list(APPEND _IMPORT_CHECK_FILES_FOR_xronos::runtime "${_IMPORT_PREFIX}/xronos/libruntime.so" )

# Import target "xronos::xronos-telemetry" for configuration "Release"
set_property(TARGET xronos::xronos-telemetry APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(xronos::xronos-telemetry PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "xronos::runtime"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/xronos/libxronos-telemetry.so"
  IMPORTED_SONAME_RELEASE "libxronos-telemetry.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS xronos::xronos-telemetry )
list(APPEND _IMPORT_CHECK_FILES_FOR_xronos::xronos-telemetry "${_IMPORT_PREFIX}/xronos/libxronos-telemetry.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
