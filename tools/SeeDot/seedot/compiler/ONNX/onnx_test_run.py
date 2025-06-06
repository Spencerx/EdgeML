# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import numpy as np
import onnxruntime
import common
import os, sys
import onnx
from onnx import helper

file_path = '../../../model/lenet/cifar-multiclass/input.onnx'
model = onnx.load(file_path)
sess = onnxruntime.InferenceSession(file_path) 

dataset_path = '../../../datasets/lenet/cifar-multiclass/test_onnx.npy'
test = np.load(dataset_path)

run_all = True
intermediate = None
 
correct = 0
total = 0

for i in range(test.shape[0] if run_all else 1):
	x = test[i,1:].reshape(-1,1)
	# x = test[i,1:].reshape(1,32,32,3).transpose(0,3,1,2).reshape(-1,1)
	output = test[i,0]

	# print(x.shape)
	# print(output)

	input_name = model.graph.input[0].name
	x = x.astype(np.float32)

	if (intermediate is not None):
		intermediate_layer_value_info = helper.ValueInfoProto()
		intermediate_layer_value_info.name = intermediate
		model.graph.output.extend([intermediate_layer_value_info])
		onnx.save(model, file_path + '_1')
		sess = onnxruntime.InferenceSession(file_path + '_1')
		pred = sess.run([intermediate_layer_value_info.name], {input_name: x})
		# np.save('debug/' + model_name + '/' + model_name + '_debug', pred)
		# with open('debug/onnx_debug.txt', 'w') as f:
		# 	f.write(common.numpy_float_array_to_float_val_str(pred))
		# print("Saving the onnx runtime intermediate output for " + intermediate_layer_value_info.name)
		print(len(pred))
		print(pred[0])
		exit()

	pred = sess.run(None, {input_name: x})

	predicted_class = pred[0][0] + 1
	print(predicted_class)
	print(int(output))

	correct += (predicted_class == int(output))
	total += 1

	# np.save('debug/' + model_name + '/' + model_name + '_output', pred)
	# with open('debug/onnx_output.txt', 'w') as f:
	# 		f.write(common.numpy_float_array_to_float_val_str(pred))
	# output_dims = common.proto_val_to_dimension_tuple(model.graph.output[0])
	# print("Saving the onnx runtime output of dimension " + str(output_dims))

print(str((float(correct)*100)/float(total)) + '% is the accuracy')
