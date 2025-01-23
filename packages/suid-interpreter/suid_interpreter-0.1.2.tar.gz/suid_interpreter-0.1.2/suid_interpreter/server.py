from suid_core import system_pb2_grpc
from suid_core import system_pb2
from suid_core.core import serve, logging
from codetiming import Timer

import cv2
import numpy as np

from worldmapping import Plane
from cartesian import *

logger = logging.getLogger("ObjectPositioningService")
class ObjectPositioningServicer(system_pb2_grpc.ObjectPositioningServicer):
    def __init__(self, plane, transposer:Object, z_diff):
        self.plane  = plane
        self.transposer = transposer
        self.transposer.crrs[0].matrices = self.plane.correlation # C2B.matrices = self.plane.correlation
        self.z_diff = z_diff

    
    @Timer("make_worldmapping",  text="{name} elapsed time: {:.4f}s", logger=logger.debug)
    def make_worldmapping(self, request, context):
        # print('gotcha')
        frame = cv2.imdecode(np.frombuffer(request.image.data, dtype = np.uint8), cv2.IMREAD_COLOR)
        self.plane.update_real_image(frame)

        image = cv2.undistort(frame, RI, DI, None, URI)
        b = cv2.fillPoly(image.copy(), plane.virtual_plane, (0,0,0))
        image = cv2.addWeighted(b, 0.4, image, 1-0.4, 0)
        
        for PR in self.plane.object_points:
            try:
                PV = self.plane.correlation._2DP(PR)
                PT = self.plane.correlation._3DP(PV)
                self.transposer.setCoordinate(camera, PV)
                _coordinate = self.transposer.getCoordinate(machine)

                cv2.circle(image, PV, 2, (0, 255, 0), -1)
                cv2.putText(image, str(PR.astype(int).flatten()[:2]), PV, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0,0,255), 1, cv2.LINE_AA)
                cv2.putText(image, f"{round(_coordinate['x'], 2)}", (PV[0],PV[1]+15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0,255,0), 1, cv2.LINE_AA)
                cv2.putText(image, f"{round(_coordinate['y'], 2)}", (PV[0],PV[1]+30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0,255,0), 1, cv2.LINE_AA)
            except AssertionError:
                print("Erro")
                pass

        centers = []
        for file in request.inference.file:
            for prediction in file.prediction:
                    print(prediction)
                    _coordinate =   np.array(
                        (
                            prediction.original_point.x*file.original_width,
                            prediction.original_point.y*file.original_height,
                            self.z_diff
                        ))
                    cv2.drawMarker(image, _coordinate.astype(int), (0,0,255), 1,20,2 )
                    self.transposer.setCoordinate(camera, _coordinate)

                    _coordinate = self.transposer.getCoordinate(machine)

                    cv2.drawMarker(image, (int(_coordinate['x']),int(_coordinate['y'])), (0,255,0), 1,20,3 )
                    centers.append(
                        {
                            'coordinate': _coordinate,
                        }
                    )
        # cv2.imwrite(f'/suid_interpreter/interpreter_ar.jpg', image)
        # cv2.imwrite(f'/suid_interpreter/interpreter.jpg', frame)
        # print(centers)
        return system_pb2.WorldMappingResult(objects=centers)

if __name__ == '__main__':
    import argparse
    import cv2.aruco as aruco
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--service_port', type=str, required=False, help="(PORT) where the this service are.", default="50051")

    parser.add_argument('--working_plane', action='store_true')
    parser.add_argument('--marker_type', type=str, required=False )
    parser.add_argument('--board_shape_width', type=str, required=False)
    parser.add_argument('--board_shape_height',type=str, required=False)
    parser.add_argument('--square_size', type=str, required=False)
    parser.add_argument('--marker_size', type=str, required=False) 
    parser.add_argument('--id_offset', type=str, required=False)
    parser.add_argument('--calibration_folder', type=str, required=True)
    parser.add_argument('--object_z_diff', type=float, default=1, required=False)
    parser.add_argument('--another_calibration_board', action='store_true')
    parser.add_argument('--calibration_square_size', type=float, default=23, required=False)
    parser.add_argument('--calibration_marker_size', type=float, default=17, required=False)
    parser.add_argument('--calibration_board_shape_width', type=int, default=8, required=False)
    parser.add_argument('--calibration_board_shape_height',type=int, default=12, required=False)
    parser.add_argument('--calibration_id_offset', type=int, default=100, required=False)

    def coords(s):
        try:
            x, y = map(float, s.split(','))
            return x, y
        except:
            raise argparse.ArgumentTypeError("Coordinates must be x,y")
        
    parser.add_argument('--board_coordinates', type=coords, nargs='*', required=True)
    parser.add_argument('--machine_coordinates', type=coords, nargs='*', required=True)

    args = parser.parse_args()
    plane = Plane(
        getattr(aruco, args.marker_type),
        (int(args.board_shape_width), int(args.board_shape_height)),
        float(args.square_size),
        float(args.marker_size),
        int(args.id_offset)
    )

    calibration_board = aruco.CharucoBoard(
        (args.calibration_board_shape_width,args.calibration_board_shape_height),
        args.calibration_square_size,
        args.calibration_marker_size,
        plane.dictionary,
        np.arange(args.calibration_id_offset, args.calibration_id_offset+int((args.calibration_board_shape_width*args.calibration_board_shape_height)/2),1)
    ) if args.another_calibration_board else None

    RI, URI, DI, ROI = plane.calibrate_from_dir(args.calibration_folder, board=calibration_board or plane.board)

    camera  = plane()
    board   = plane(args.board_coordinates)
    machine = plane(args.machine_coordinates)

    C2B = CameraCorrelation(camera, board)
    B2M = BoardCorrelation(board, machine)

    transposer = Object(C2B, B2M)

    servicer = ObjectPositioningServicer(plane,transposer, args.object_z_diff)
    serve(system_pb2_grpc.add_ObjectPositioningServicer_to_server, servicer, logger, server_port=args.service_port)