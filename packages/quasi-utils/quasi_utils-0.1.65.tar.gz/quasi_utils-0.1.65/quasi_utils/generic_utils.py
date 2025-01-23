import decimal
import gzip
import json
import pickle
import shutil


class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return str(o)
		
		return super().default(o)


def uncompress(zip_path, file_path):
	with gzip.open(zip_path, 'rb') as f_in:
		with open(file_path, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)


def text_to_pickle(text, direc):
	with open(direc, 'wb') as f:
		pickle.dump(text, f)


def pickle_to_text(direc):
	with open(direc, 'rb') as f:
		return pickle.load(f)


def colourise(text, colour, decorate=None, end_='\n'):
	_c = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'grey': '\033[97m',
	      'cyan': '\033[96m', 'end': '\033[0m', 'red': '\033[91m', 'underline': '\033[4m', 'bold': '\033[1m'}
	colour, end = _c[colour], _c['end']
	
	if decorate is not None:
		print(f'{_c[decorate]}{colour}{text}{end}', end=end_)
	else:
		print(f'{colour}{text}{end}', end=end_)


def special_format(n):
	s, *d = str(n).partition('.')
	r = ','.join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
	ans = ''.join([r] + d)
	
	if ans.startswith('-,'):
		ans2 = ans.replace('-,', '-')
		
		return ans2
	
	return ans
