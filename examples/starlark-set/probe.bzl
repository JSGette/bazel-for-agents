def _set_probe_impl(ctx):
    values = set(["beta", "alpha", "beta"])
    if len(values) != 2 or "alpha" not in values:
        fail("set constructor or membership failed")
    values.add("gamma")
    union = values | set(["delta", "alpha"])
    if len(union) != 4:
        fail("set union failed")
    out = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(out, "\n".join(sorted(union)) + "\n")
    return [DefaultInfo(files = depset([out]))]

set_probe = rule(implementation = _set_probe_impl)
