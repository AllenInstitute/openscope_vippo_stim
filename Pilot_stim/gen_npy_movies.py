import numpy as np
from scipy.ndimage import rotate
class BarVideoGenerator:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def create_video(self, speed, direction):
        duration = speed  # Duration is directly provided in seconds
        fps = 60
        num_frames = int(duration * fps)
        frames = np.zeros((num_frames, self.height, self.width), dtype=np.uint8)
        for i in range(num_frames):
            y = int((i / float(num_frames)) * self.height)
            x = int((i / float(num_frames)) * self.width)

            if direction == 'up_down':
                frames[i, y:(y + self.height//12), :] = 255  # Set the bar color to white
            elif direction == 'down_up':
                frames[i, (self.height - y - self.height//12):(self.height - y), :] = 255
            elif direction == 'left_right':
                frames[i, :, x:(x + self.width//12)] = 255
            elif direction == 'right_left':
                frames[i, :, (self.width - x - self.width//12):(self.width - x)] = 255
            elif direction == 'cr' or direction == 'acr':
                if self.height<self.width:
                    bar_length = self.height 
                else:
                    bar_length = self.width
                bar_width = self.width // 12  # Set the width of the rotating bar as one-twelfth of the screen width
                angle = float(360) / float(num_frames)
                x_center = self.width // 2
                y_center = self.height // 2
                x_start = int(x_center - bar_length // 2)
                x_end = int(x_center + bar_length // 2 )
                y_start = int(y_center - bar_width // 2)
                y_end = int(y_center + bar_width // 2)
                frames[i, y_start:y_end, x_start:x_end] = 255
                if direction == 'cr':
                    if i:
                        frames[i] = rotate(frames[i-1], angle, reshape=False, cval=0)
                else:
                    if i:
                        frames[i] = rotate(frames[i-1], angle, reshape=False, cval=0)
            elif direction == 'div_pos':
                x_center = self.width // 2
                y_center = self.height // 2
                smaller_dim = 0
                if self.width>self.height:
                    smaller_dim = self.height
                else:
                    smaller_dim = self.width
                radius_max = smaller_dim/2
                radius_min = smaller_dim/10
                radius_step = (float(radius_max) - float(radius_min))/float(num_frames)
                if i==0:
                    radius = radius_min
                radius += float(radius_step)
                y, x = np.ogrid[:self.height, :self.width]
                dist = np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
                mask = dist <= float(radius)
                frames[i,mask] = 255  # Set the white dot within the radius
            elif direction == 'div_neg':
                x_center = self.width // 2
                y_center = self.height // 2
                smaller_dim = 0
                if self.width>self.height:
                    smaller_dim = self.height
                else:
                    smaller_dim = self.width
                radius_max = smaller_dim/2
                radius_min = smaller_dim/10
                radius_step = (float(radius_max) - float(radius_min))/float(num_frames)
                if i==0:
                    radius = radius_max
                radius -= float(radius_step)
                # Calculate the radius based on the current frame
                y, x = np.ogrid[:self.height, :self.width]
                dist = np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
                mask = dist <= radius
                frames[i,mask] = 255  # Set the white dot within the radius
            #elif direction == 'flicker':
            #elif direction == 'disco':
            #elif direciton == 'movie':
        return frames

    def generate_videos(self, generate_all):
        speeds = [10, 2, 0.6]  # Low, medium, and high speeds
        directions = ['up_down', 'down_up', 'left_right', 'right_left', 'cr', 'acr','div_pos','div_neg']
        if generate_all:
            for direction in directions:
                for speed in speeds:
                    video = self.create_video(speed, direction)
                    file_name = 'Movies/' + direction + '_speed_' + str(speed) + '.npy'
                    np.save(file_name, video)
        else:
            direction = input('Enter the direction (up_down, down_up, left_right, right_left, clockwise_rotation, anticlockwise_rotation): ')
            speed = float(input('Enter the speed (in seconds): '))
            video = self.create_video(speed, direction)
            file_name = 'Movies/' + direction + '_speed_' + str(speed) + '.npy'
            np.save(file_name, video)
            
generator = BarVideoGenerator(height=1080, width=1920)
generator.generate_videos(generate_all=False)