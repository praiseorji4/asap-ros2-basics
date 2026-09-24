# Count.msg - one tick of a counter node.
int64 count                     # the number
string source                   # which node counted (its name)
builtin_interfaces/Time stamp   # when it counted
