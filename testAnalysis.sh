#!/bin/bash
coverage run --source='./calendar_app' manage.py test calendar_app >/dev/null 2>/dev/null
mkdir -p ./testAnalysis

echo $'Coverage report: \n' > ./testAnalysis/coverageReport.txt
coverage report >> ./testAnalysis/coverageReport.txt

echo $'Cyclomatic Complexity: \n' > ./testAnalysis/ccReport.txt
radon cc calendar_app >> ./testAnalysis/ccReport.txt

echo $'ABC score: \n' > ./testAnalysis/abcReport.txt
radon cc -a -s calendar_app >> ./testAnalysis/abcReport.txt

echo $'Maintainability Index: \n' > ./testAnalysis/miReport.txt
radon mi -i A calendar_app >> ./testAnalysis/miReport.txt

echo $'Halstead Complexity: \n' > ./testAnalysis/halReport.txt
radon hal calendar_app >> ./testAnalysis/halReport.txt

echo $'Raw Metrics: \n' > ./testAnalysis/rawReport.txt
radon raw calendar_app >> ./testAnalysis/rawReport.txt