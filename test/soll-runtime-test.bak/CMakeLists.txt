# SPDX-License-Identifier: Apache-2.0

#add_executable(evmcTest2
#  evmcTest2.cpp
#)
#
#target_link_libraries(evmcTest2
#  soll_runtime_test
#  ssvmSupport
#  ssvmEVMCUtilEVMCLoader
#  utilGoogleTest
#  ${CMAKE_DL_LIBS}
#)
#
#target_include_directories(evmcTest2
#  PRIVATE
#  ${SSVM_CORE_SRC_DIR}/include
#  ${PROJECT_SOURCE_DIR}/include
#)


add_library(soll_runtime_test SHARED
  evmcTest.cpp
  example_host.cpp
)

target_link_libraries(soll_runtime_test
  PRIVATE
  ssvmSupport
  ssvmEVMCUtilEVMCLoader
  utilGoogleTest
  ${CMAKE_DL_LIBS}
)

target_include_directories(soll_runtime_test
  PRIVATE
  ${SSVM_CORE_SRC_DIR}/include
  ${PROJECT_SOURCE_DIR}/include
)
