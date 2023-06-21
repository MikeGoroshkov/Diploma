import pygame

pygame.init()

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512, devicename=None)
intro_sound = pygame.mixer.Sound('sounds/Overrated.mp3')
bg_sound = pygame.mixer.Sound('sounds/Loops_Of_Fury.mp3')
blaster_sound = pygame.mixer.Sound('sounds/laser-blast.mp3')
key_sound = pygame.mixer.Sound('sounds/key.mp3')
arrow_sound = pygame.mixer.Sound('sounds/arrow.mp3')
sip_sound = pygame.mixer.Sound('sounds/sip.mp3')
key_card_sound = pygame.mixer.Sound('sounds/key_card.mp3')

# def play_music(music_file):
#     """
#     stream music with mixer.music module in blocking manner
#     this will stream the sound from disk while playing
#     """
#     clock = pygame.time.Clock()
#     try:
#         pygame.mixer.music.load(music_file)
#         print ("Music file %s loaded!" % music_file)
#     except pygame.error:
#         print ("File %s not found! (%s)" % (music_file, pygame.get_error()))
#         return
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         # check if playback has finished
#         clock.tick(30)

# play_music("sounds/Loops_Of_Fury.mid")
