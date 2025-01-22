// SPDX-FileCopyrightText: Copyright (c) 2025 Xronos Inc.
// SPDX-License-Identifier: BSD-3-Clause

#ifndef RUNTIME_MISC_ELEMENT_HH
#define RUNTIME_MISC_ELEMENT_HH

#include "runtime/reactor_element.hh"

namespace reactor {

// An element that is not directly relevant to the runtime. Can be used to
// create additional elements that behave similarly to the core runtime
// elements, but that do not impact the execution behavior.
class MiscElement : public ReactorElement {

public:
  MiscElement(std::string_view name, Reactor& container)
      : ReactorElement(name, container) {}

  void startup() override {}
  void shutdown() override {}

  void visit(ReactorElementVisitor& visitor) const final { visitor.visit(*this); };
};

} // namespace reactor

#endif // RUNTIME_MISC_ELEMENT_HH
