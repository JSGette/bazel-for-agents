"""Small rules illustrating analysis-time interfaces and producing actions."""

GreetingInfo = provider(
    doc = "A generated greeting and the person it addresses.",
    fields = {
        "message": "File containing the generated greeting.",
        "person": "String naming the addressee.",
    },
)

def _greeting_impl(ctx):
    message = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.expand_template(
        template = ctx.file.template,
        output = message,
        substitutions = {"{NAME}": ctx.attr.person},
    )

    metadata = ctx.actions.declare_file(ctx.label.name + ".metadata.txt")
    ctx.actions.write(metadata, "person=" + ctx.attr.person + "\n")

    return [
        GreetingInfo(message = message, person = ctx.attr.person),
        DefaultInfo(
            files = depset([message]),
            runfiles = ctx.runfiles(files = [ctx.file.runtime_data]),
        ),
        OutputGroupInfo(metadata = depset([metadata])),
    ]

greeting = rule(
    implementation = _greeting_impl,
    provides = [GreetingInfo],
    attrs = {
        "person": attr.string(mandatory = True),
        "runtime_data": attr.label(allow_single_file = True, mandatory = True),
        "template": attr.label(allow_single_file = True, mandatory = True),
    },
)

def _greeting_report_impl(ctx):
    source = ctx.attr.source
    greeting_info = source[GreetingInfo]
    defaults = source[DefaultInfo]

    # These checks exercise provider contents without reading artifact contents.
    if defaults.files.to_list() != [greeting_info.message]:
        fail("the greeting must expose only its message as a default output")
    runtime_files = defaults.default_runfiles.files.to_list()
    if len(runtime_files) != 1 or runtime_files[0].basename != "runtime.txt":
        fail("runtime data must be available separately in runfiles")

    report = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.expand_template(
        template = greeting_info.message,
        output = report,
        substitutions = {"Hello": "Greetings"},
    )
    return [DefaultInfo(
        files = depset([report]),
        runfiles = ctx.runfiles().merge(defaults.default_runfiles),
    )]

greeting_report = rule(
    implementation = _greeting_report_impl,
    attrs = {
        "source": attr.label(mandatory = True, providers = [GreetingInfo]),
    },
)
