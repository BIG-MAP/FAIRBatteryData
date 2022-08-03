clear all
close all
clc

bat = DataModel('BatteryCellMetadata.json');
bat.load('battery_cell_profile.json')