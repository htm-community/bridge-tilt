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
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import nupic_anomaly_output


MODEL_NAME = "TiltTemp2009"
DATA_DIR = "./data"
MODEL_PARAMS_DIR = "./model_params"
PREDICTED_FIELD = "Tilt_06"
# '7/2/10 0:00'
DATE_FORMAT = "%m/%d/%y %H:%M"

_METRIC_SPECS = (
    MetricSpec(field=PREDICTED_FIELD, metric="multiStep",
               inferenceElement="multiStepBestPredictions",
               params={"errorMetric": "aae", "window": 1000, "steps": 1}),
    MetricSpec(field=PREDICTED_FIELD, metric="trivial",
               inferenceElement="prediction",
               params={"errorMetric": "aae", "window": 1000, "steps": 1}),
    MetricSpec(field=PREDICTED_FIELD, metric="multiStep",
               inferenceElement="multiStepBestPredictions",
               params={"errorMetric": "altMAPE", "window": 1000, "steps": 1}),
    MetricSpec(field=PREDICTED_FIELD, metric="trivial",
               inferenceElement="prediction",
               params={"errorMetric": "altMAPE", "window": 1000, "steps": 1}),
)

def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": PREDICTED_FIELD})
  return model



def getModelParamsFromName(modelName):
  importName = "model_params.%s_model_params" % (
    modelName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % modelName)
  return importedModelParams



def runIoThroughNupic(inputData, model, modelName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  headers = csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_anomaly_output.NuPICPlotOutput(modelName)
  else:
    output = nupic_anomaly_output.NuPICFileOutput(modelName)

  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())

  counter = 0
  for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    consumption = float(row[1])
    result = model.run({
      "Time": timestamp,
      PREDICTED_FIELD: consumption
    })
    result.metrics = metricsManager.update(result)

    if counter % 100 == 0:
      print "Read %i lines..." % counter
      print ("After %i records, 1-step altMAPE=%f", counter,
              result.metrics["multiStepBestPredictions:multiStep:"
                             "errorMetric='altMAPE':steps=1:window=1000:"
                             "field=%s" % PREDICTED_FIELD])
 
    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    output.write(timestamp, consumption, prediction, anomalyScore)

  inputFile.close()
  output.close()



def runModel(modelName, plot=False):
  print "Creating model from %s..." % modelName
  model = createModel(getModelParamsFromName(modelName))
  inputData = "%s/%s.csv" % (DATA_DIR, modelName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, modelName, plot)



if __name__ == "__main__":
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(MODEL_NAME, plot=plot)