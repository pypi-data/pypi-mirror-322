function(tweak_target tweaked)
  # EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a define (VERSION_INFO) here.
  target_compile_definitions(${tweaked} PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

  target_include_directories(${tweaked} PRIVATE ${CORE_DIR}/src)

  target_include_directories(${tweaked} PRIVATE ${CORE_DIR}/glm)

  target_include_directories(${tweaked} PRIVATE ${CORE_DIR}/JoltPhysics)
  target_link_libraries(${tweaked} PRIVATE Jolt)

  if(MSVC)
    target_compile_options(${tweaked} PRIVATE /W4)
  else()
    target_compile_options(${tweaked} PRIVATE -Wall -Wextra -Wpedantic -fPIC)
  endif()

  if(MSVC)
    target_compile_options(${tweaked} PRIVATE /Zi)
  else()
    target_compile_options(${tweaked} PRIVATE -g)
  endif()
endfunction()
