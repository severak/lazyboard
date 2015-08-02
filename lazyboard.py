import pygame
import pygame.midi
import ConfigParser

def main():
	chords = {}
	# C, G, Ami, F
	#chords["c"] = [60, 64, 67] 
	#chords["d"] = [62, 66, 69] 
	#chords["g"] = [67, 71, 74]
	#chords["f"] = [66, 69, 72]
	# Ami
	#chords["a"] = [69, 72, 76]
	# Emi
	#chords["e"] = [64, 67, 71]
	
	pygame.init()
	#pygame.event.set_blocked(MOUSEMOTION)
	
	pygame.display.set_mode((300, 200))
	pygame.display.set_caption("LazyBoard")
	pygame.display.flip()
	
	config = ConfigParser.RawConfigParser()
	config.optionxform = str
	config.read("lazyboard.ini")
	
	chords_def = {}
	for chord_name, chord_def in config.items("chords"):
		chdef = []
		for i in chord_def.split(" "):
			chdef.append(int(i))
		chords_def[chord_name] = chdef
	print repr(chords_def)
	for key, chord_name in config.items("keys"):
		print chord_name
		if chord_name in chords_def:
			chords[key] = chords_def[chord_name]
	
	
	
	pygame.midi.init()
	port = pygame.midi.get_default_output_id()
	if config.has_option("lazyboard","device_id"):
		port = config.getint("lazyboard","device_id")
	instrument = 0
	if config.has_option("lazyboard","instrument"):
		instrument = config.getint("lazyboard","instrument")
	midi_out = pygame.midi.Output(port, latency=0)
	midi_out.set_instrument(instrument, 1)
	keycounter = [0] * 128
	while 1:
		e = pygame.event.wait()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				print "Konec"
				break
			else:
				if chr(e.key) in chords:
					for i in chords[chr(e.key)]:
						if keycounter[i]==0:
							midi_out.note_on(i, 127, 1)
						keycounter[i] += 1
		elif e.type == pygame.KEYUP:
			if chr(e.key) in chords:
				for i in chords[chr(e.key)]:
					keycounter[i] -= 1
					if keycounter[i]==0:
						midi_out.note_off(i, 0, 1)
		elif e.type == pygame.QUIT:
			break
	del midi_out
	pygame.midi.quit()
	return None
			
if __name__ == '__main__':
	main()