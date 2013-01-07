
def is_live(data):
	tags = data.get("tags", [])

	for tag in tags:
		id = tag.get("id", "")

		if "tone/minutebyminute" in id:
			return True

	return False