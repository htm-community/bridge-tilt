MODEL_PARAMS = {

  'aggregationInfo': {
    'days': 0,
    'fields': [('Tilt_06', 'sum')],
    'hours': 1,
    'microseconds': 0,
    'milliseconds': 0,
    'minutes': 0,
    'months': 0,
    'seconds': 0,
    'weeks': 0,
    'years': 0
  },

  'model': 'CLA',

  'modelParams': {

    'anomalyParams': {
      'anomalyCacheRecords': None,
      'autoDetectThreshold': None,
      'autoDetectWaitRecords': None},

    'clParams': {
      'regionName': 'CLAClassifierRegion',

      # Classifier diagnostic output verbosity control;
      # 0: silent; [1..6]: increasing levels of verbosity
      'clVerbosity': 0,

      # This controls how fast the classifier learns/forgets. Higher values
      # make it adapt faster and forget older patterns faster.
      'alpha': 0.0001,

      # This is set after the call to updateConfigFromSubConfig and is
      # computed from the aggregationInfo and predictAheadTime.
      'steps': '1,5',

      'implementation': 'cpp',
    },

    'inferenceType': 'TemporalAnomaly',

    'sensorParams': {
      'encoders': {
        'Tilt_06': {
          'fieldname': 'Tilt_06',
          'resolution': 0.88,
          'seed': 1,
          'name': 'Tilt_06',
          'type': 'RandomDistributedScalarEncoder',
        },
        'Time_timeOfDay': {
          'fieldname': 'Time',
          'name': 'Time_timeOfDay',
          'timeOfDay': (21, 1),
          'type': 'DateEncoder'
        },
        'Time_weekend': {
          'fieldname': 'Time',
          'name': 'Time_weekend',
          'type': 'DateEncoder',
          'weekend': 21
        }
      },
      'sensorAutoReset': None,
      'verbosity': 0
    },

    'spEnable': True,

    'spParams': {
      # SP diagnostic output verbosity control;
      # 0: silent; >=1: some info; >=2: more info;
      'spVerbosity': 0,

      # Spatial Pooler implementation selector.
      # Options: 'py', 'cpp' (speed optimized, new)
      'spatialImp': 'cpp',

      'globalInhibition': 1,

      # Number of cell columns in the cortical region (same number for
      # SP and TP)
      # (see also tpNCellsPerCol)
      'columnCount': 2048,

      'inputWidth': 0,

      # SP inhibition control (absolute value);
      # Maximum number of active columns in the SP region's output (when
      # there are more, the weaker ones are suppressed)
      'numActiveColumnsPerInhArea': 40,

      'seed': 1956,

      # potentialPct
      # What percent of the columns's receptive field is available
      # for potential synapses.
      'potentialPct': 0.85,

      # The default connected threshold. Any synapse whose
      # permanence value is above the connected threshold is
      # a "connected synapse", meaning it can contribute to the
      # cell's firing. Typical value is 0.10.
      'synPermConnected': 0.1,

      'synPermActiveInc': 0.04,

      'synPermInactiveDec': 0.005,
    },

    'tpEnable': True,

    'tpParams': {
      # TP diagnostic output verbosity control;
      # 0: silent; [1..6]: increasing levels of verbosity
      # (see verbosity in nta/trunk/py/nupic/research/TP.py and TP10X*.py)
      'verbosity': 0,

      # Number of cell columns in the cortical region (same number for
      # SP and TP)
      # (see also tpNCellsPerCol)
      'columnCount': 2048,

      # The number of cells (i.e., states), allocated per column.
      'cellsPerColumn': 32,

      'inputWidth': 2048,

      'seed': 1960,

      # Temporal Pooler implementation selector (see _getTPClass in
      # CLARegion.py).
      'temporalImp': 'cpp',

      # New Synapse formation count
      # NOTE: If None, use spNumActivePerInhArea
      #
      # TODO: need better explanation
      'newSynapseCount': 20,

      # Maximum number of synapses per segment
      # > 0 for fixed-size CLA
      # -1 for non-fixed-size CLA
      #
      # TODO: for Ron: once the appropriate value is placed in TP
      # constructor, see if we should eliminate this parameter from
      # description.py.
      'maxSynapsesPerSegment': 32,

      # Maximum number of segments per cell
      # > 0 for fixed-size CLA
      # -1 for non-fixed-size CLA
      #
      # TODO: for Ron: once the appropriate value is placed in TP
      # constructor, see if we should eliminate this parameter from
      # description.py.
      'maxSegmentsPerCell': 128,

      # Initial Permanence
      # TODO: need better explanation
      'initialPerm': 0.21,

      # Permanence Increment
      'permanenceInc': 0.1,

      # Permanence Decrement
      # If set to None, will automatically default to tpPermanenceInc
      # value.
      'permanenceDec': 0.1,

      'globalDecay': 0.0,

      'maxAge': 0,

      # Minimum number of active synapses for a segment to be considered
      # during search for the best-matching segments.
      # None=use default
      # Replaces: tpMinThreshold
      'minThreshold': 12,

      # Segment activation threshold.
      # A segment is active if it has >= tpSegmentActivationThreshold
      # connected synapses that are active due to infActiveState
      # None=use default
      # Replaces: tpActivationThreshold
      'activationThreshold': 16,

      'outputType': 'normal',

      # "Pay Attention Mode" length. This tells the TP how many new
      # elements to append to the end of a learned sequence at a time.
      # Smaller values are better for datasets with short sequences,
      # higher values are better for datasets with long sequences.
      'pamLength': 1,
    },

    'trainSPNetOnlyIfRequested': False
  },

  'predictAheadTime': None,
  'version': 1
}