enable_testing()

add_executable(core_tests "test_object.cpp" "test_world.cpp" "test_ragdoll.cpp")

target_link_libraries(core_tests PRIVATE core_src)

tweak_target(core_tests)

target_link_libraries(core_tests PRIVATE GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(core_tests)
