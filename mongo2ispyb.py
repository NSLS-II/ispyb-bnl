import lsdb2
import db_lib
import ispyb.factory
from datetime import datetime
import sys

conf_file = 'config.cfg'
# visit = sys.argv[1]
visit = 'mx30816-1'

# Get a list of request dicts
request_dicts = lsdb2.getColRequestsByTimeInterval('2018-02-14T00:00:00','2018-02-15T00:00:00')

# Connect to ISPyB, get the relevant data area objects
with ispyb.open(conf_file) as conn:
  core = ispyb.factory.create_data_area(ispyb.factory.DataAreaType.CORE, conn)
  mxacquisition = ispyb.factory.create_data_area(ispyb.factory.DataAreaType.MXACQUISITION, conn)

  # Find the id for a particular
  sessionid = core.retrieve_visit_id(visit)

  # Parsing the requests
  for request in request_dicts:
     request_type = request['request_type']

     # We're only interested in standard and vector requests for now .....
     if request_type in('standard', 'vector') :
         sample = request['sample'] # this needs to be created and linked to a DC group


         reqres = db_lib.getResultsforRequest(request['uid'])

         for result in reqres:
             if result['result_type'] == 'mxExpParams':
                 result_obj = result['result_obj']
                 request_obj = result_obj['requestObj']

                 # Create a new data collection group entry:
                 params = mxacquisition.get_data_collection_group_params()
                 params['parentid'] = sessionid
                 # params['sampleid'] = ?
                 if request_type == 'standard':
                     params['experimenttype'] = 'OSC'
                 elif request_type == 'vector':
                     params['experimenttype'] = 'Helical'

                 params['starttime'] = datetime.utcfromtimestamp(request['time']).strftime('%Y-%m-%d %H:%M:%S')
                 params['endtime'] = datetime.utcfromtimestamp(request['time']).strftime('%Y-%m-%d %H:%M:%S')
                 dcg_id = mxacquisition.insert_data_collection_group(list(params.values()))
                 print("dcg_id: %i" % dcg_id)

                 params = mxacquisition.get_data_collection_params()
                 params['parentid'] = dcg_id
                 params['visitid'] = sessionid
                 params['imgdir'] = request_obj['directory']
                 params['imgprefix'] = request_obj['file_prefix']
                 params['imgsuffix'] = 'cbf' # assume CBF ...?
                 params['wavelength'] = request_obj['wavelength']
                 params['starttime'] = datetime.utcfromtimestamp(request['time']).strftime('%Y-%m-%d %H:%M:%S')

                 params['run_status'] = 'DataCollection Successful' # assume success / not aborted
                 params['datacollection_number'] = request_obj['runNum']
                 params['n_images'] = int(round((request_obj['sweep_end'] - request_obj['sweep_start']) / request_obj['img_width']))
                 params['exp_time'] = request_obj['exposure_time']
                 params['start_image_number'] = request_obj['file_number_start']

                 params['axis_start'] = request_obj['sweep_start']
                 params['axis_end'] = request_obj['sweep_end']
                 params['axis_range'] = request_obj['img_width']
                 params['resolution'] = request_obj['resolution']

                 params['detector_distance'] = request_obj['detDist']
                 params['slitgap_horizontal'] = request_obj['slit_width']
                 params['slitgap_vertical'] = request_obj['slit_height']

                 params['transmission'] = request_obj['attenuation']

                 # params['file_template'] = ?

                 # params['flux'] = ?

                 # hacrd-coding hack to make SynchWeb understand whether it's a full data collection or a screening
                 if request_type == 'screening':
                     params['overlap'] = 89.0
                 else:
                     params['overlap'] = 0.0

                 # params['xbeam'] = ?
                 # params['ybeam'] = ?
                 # params['beamsize_at_samplex'] = ?
                 # params['beamsize_at_sampley'] = ?
                 # params['rotation_axis'] = ?
                 # params['phistart'] = ?
                 # params['kapppastart'] = ?
                 # params['omegastart'] = ?

                 params['xtal_snapshot1'] = '/dls/i03/data/2016/cm14451-2/jpegs/20160413/test_xtal/xtal1_1_1_0.0.png'
                 params['xtal_snapshot2'] = '/dls/i03/data/2016/cm14451-2/jpegs/20160413/test_xtal/xtal1_1_1_90.0.png'
                 params['xtal_snapshot3'] = '/dls/i03/data/2016/cm14451-2/jpegs/20160413/test_xtal/xtal1_3_1_183.0.png'
                 params['xtal_snapshot4'] = '/dls/i03/data/2016/cm14451-2/jpegs/20160413/test_xtal/xtal1_3_1_93.0.png'

                 dc_id = mxacquisition.insert_data_collection(list(params.values()))
                 print("dc_id: %i" % dc_id)
