#!/bin/sh


# Чтобы Redis автоматически на сервере не отключался из-за предупреждения, которое
# будет оповещать об возникновении ошибки, когда произойдет сохранение при низком
# уровне памяти.
sysctl vm.overcommit_memory=1