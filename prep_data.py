#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import sys
import os
import csv
import datetime
import pprint


OUTPUT_DIR = "./data"
INPUT_DATE_FORMAT = "%d-%b-%Y %H:%M:%S"
OUTPUT_DATE_FORMAT = "%m/%d/%y %H:%M"
SWARM_DESCRIPTION_OUT = "./swarm_description.py"


SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "Time",
      "fieldType": "datetime"
    },
  ],
  "streamDef": {
    "info": "bridge_tilt",
    "version": 1,
    "streams": [
      {
        "info": "Bridge Tilt",
        # "source": "file://rec-center-hourly.csv",
        "source": "",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "Tilt_06"
  },
  "iterationCount": 2000,
  "swarmSize": "medium"
}


def run(inputFilePath):
  name = os.path.splitext(os.path.basename(inputFilePath))[0]
  inputFile = open(inputFilePath, "rb")
  outputFile = os.path.join(OUTPUT_DIR, "%s.csv" % name)
  csvReader = csv.reader(inputFile)
  headers = csvReader.next()
  minValues = {}
  maxValues = {}
  pp = pprint.PrettyPrinter(indent=2)

  for header in headers[1:]:
    minValues[header] = None;
    maxValues[header] = None;

  with open(outputFile, "w") as output:
    output.write(",".join(headers) + "\n")
    types = "datetime,%s\n" % ",".join(["float" for field in headers[1:]])
    flags = "T,%s\n" % ",".join(["" for field in headers[1:]])
    output.write(types)
    output.write(flags)

    for row in csvReader:
      dataValues = [float(v) for v in row[1:]]
      for i, value in enumerate(dataValues):
        currentMin = minValues[headers[i+1]]
        currentMax = maxValues[headers[i+1]]
        if currentMin is None or value < currentMin:
          minValues[headers[i+1]] = value
        if currentMax is None or value > currentMax:
          maxValues[headers[i+1]] = value;
      timestamp = datetime.datetime.strptime(row[0], INPUT_DATE_FORMAT)
      timeOut = timestamp.strftime(OUTPUT_DATE_FORMAT)
      output.write("%s,%s\n" % (timeOut, ",".join(row[1:])))

  for dataHeader in headers[1:]:
    SWARM_DESCRIPTION["includedFields"].append({
      "fieldName": dataHeader,
      "fieldType": "float",
      "minValue": minValues[dataHeader],
      "maxValue": maxValues[dataHeader]
    })

  SWARM_DESCRIPTION["streamDef"]["streams"][0]["source"] = \
    "file://%s" % os.path.abspath(os.path.join(outputFile))

  with open(SWARM_DESCRIPTION_OUT, "w") as swarmOut:
    swarmOut.write("SWARM_DESCRIPTION = %s" % pp.pformat(SWARM_DESCRIPTION))

  print "\nOutput file ready for NuPIC at %s." % outputFile
  print "\nSwarm description ready for NuPIC at %s." % SWARM_DESCRIPTION_OUT



if __name__ == "__main__":
  args = sys.argv[1:]
  
  try:
    inputFile = args[0]
  except IndexError:
    print "Please provide path to input file as cmd line parameter."
    exit(-1)
  
  run(inputFile)