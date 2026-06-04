def replace_wisdom_hub():
    print("Updating wisdom_hub.html Article 4...")
    content = open("wisdom_hub.html", encoding="utf-8").read()
    
    # Locate Article 4 (id: 4)
    start_idx = content.find("id: 4")
    if start_idx == -1:
        print("  [ERROR] id: 4 not found in wisdom_hub.html")
        return
        
    # Find 'content: ' after id: 4
    content_idx = content.find("content: '", start_idx)
    if content_idx == -1:
        print("  [ERROR] content: ' not found in wisdom_hub.html Article 4")
        return
    
    str_start = content_idx + len("content: '")
    # Find the closing "'" followed by "," and "image_url:"
    str_end = content.find("',", str_start)
    while str_end != -1:
        after_str = content[str_end:str_end+100]
        if "image_url" in after_str:
            break
        str_end = content.find("',", str_end + 1)
        
    if str_end == -1:
        print("  [ERROR] End of content string not found in wisdom_hub.html Article 4")
        return
        
    new_body = """<h3>The Sacred Texts of Nagara Nirmana</h3><p>While the term 'Samhita' broadly refers to compendiums or collections of knowledge, the rules for building a divine city are found across Shilpa Shastras (architectural manuals), Agamas (temple and societal codes), and Puranic Samhitas.</p><h4>A. The Shilpa Shastras (The Architectural Manuals)</h4><ul><li><b>Manasara (Manasara Shilpa Shastra):</b> This is the ultimate encyclopedia of Vastu. It contains a specific section called Nagara Vidhana (Rules for Towns). It categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li><li><b>Mayamatam (Mayamata):</b> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li><li><b>Samarangana Sutradhara:</b> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li><li><b>Aparajita Priccha:</b> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li></ul><h4>B. The Samhitas and Puranas</h4><ul><li><b>Brihat Samhita (by Varahamihira):</b> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li><li><b>Vishnudharmottara Purana:</b> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li><li><b>Agni Purana & Matsya Purana:</b> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li></ul><h4>C. The Agamas (The Living Codes of the Temple City)</h4><ul><li><b>Kamikagama, Karanagama, and Suprabhedagama:</b> In South India, the Agamas are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the Prakaras (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</li></ul><h3>The Blueprint: How the 'Divine Reality' is Built</h3><p>According to these texts, a divine city is built using the Vastu Purusha Mandala. For a major city, a grid of 81 squares (9x9), known as the <b>Paramasayika mandala</b>, is drawn on the earth.</p><ul><li><b>The Brahmasthana (The Divine Center):</b> The central squares of the grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple. This is the anchor of the city.</li><li><b>The Prakaras (The Concentric Layers):</b> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li><li><b>The Zoning of Samsara (Worldly Life):</b><ul><li><i>Inner Ring:</i> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li><li><i>Middle Ring:</i> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the engine of society).</li><li><i>Outer Ring:</i> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li><li><i>The Periphery:</i> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li></ul></li></ul><h3>The Ultimate Example: Madurai Sthalam</h3><p>Madurai is the flawless, living embodiment of the Mayamatam and the Agamas. It is known in the texts as a <b>Padma Vana</b> (Lotus Forest) or <b>Kudal</b> (The Confluence).</p><ul><li><b>The Center (The Pistil of the Lotus):</b> At the absolute Brahmasthana sits the Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless Consciousness, and Shakti (Meenakshi) represents the dynamic Energy of the universe. They are the still point of the turning world.</li><li><b>The Streets (The Petals of the Lotus):</b> Radiating outward from the temple are concentric rectangular streets, named after the Tamil months: Chitrai Veedhi (Innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (Outermost).</li><li><b>The Transformation of Samsara into Dharma:</b> In a modern city, the center is usually a bank, a mall, or a corporate plaza (representing greed and commerce). In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing Pradakshina (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce of the outer streets is protected and sanctified by the stillness of the inner sanctum.</li><li><b>The Water Element:</b> The texts demand a water body for purification. Madurai is built on the banks of the Vaigai River, and the temple itself houses the Potramarai Kulam (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality).</li></ul><h3>Summary: Environment Dictates Consciousness</h3><p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: Environment dictates consciousness. If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara gets, is always held in the loving, gravitational embrace of the Divine.</p>"""
    
    new_content = content[:str_start] + new_body + content[str_end:]
    with open("wisdom_hub.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("  [SUCCESS] Updated wisdom_hub.html")

def replace_server():
    print("Updating server.py Article 4...")
    content = open("server.py", encoding="utf-8").read()
    
    # Find the title string in server.py
    title_idx = content.find('"The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built",')
    if title_idx == -1:
        print("  [ERROR] Title not found in server.py")
        return
        
    # Find the next double quote after title_idx (which starts the summary)
    summary_idx = content.find('"', title_idx + len('"The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built",'))
    if summary_idx == -1:
        print("  [ERROR] Summary quote not found in server.py")
        return
        
    # Find the end of summary quote
    summary_end = content.find('",', summary_idx + 1)
    if summary_end == -1:
        print("  [ERROR] Summary end quote not found in server.py")
        return
        
    # Find the content double quote after summary_end
    content_idx = content.find('"', summary_end + 2)
    if content_idx == -1:
        print("  [ERROR] Content quote not found in server.py")
        return
        
    str_start = content_idx + 1
    # Find the closing quote followed by "," and "sacred_city.png"
    str_end = content.find('",', str_start)
    while str_end != -1:
        after_str = content[str_end:str_end+100]
        if "sacred_city.png" in after_str:
            break
        str_end = content.find('",', str_end + 1)
        
    if str_end == -1:
        print("  [ERROR] End of content string not found in server.py")
        return
        
    new_body = """<h3>The Sacred Texts of Nagara Nirmana</h3><p>While the term 'Samhita' broadly refers to compendiums or collections of knowledge, the rules for building a divine city are found across Shilpa Shastras (architectural manuals), Agamas (temple and societal codes), and Puranic Samhitas.</p><h4>A. The Shilpa Shastras (The Architectural Manuals)</h4><ul><li><b>Manasara (Manasara Shilpa Shastra):</b> This is the ultimate encyclopedia of Vastu. It contains a specific section called Nagara Vidhana (Rules for Towns). It categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li><li><b>Mayamatam (Mayamata):</b> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li><li><b>Samarangana Sutradhara:</b> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li><li><b>Aparajita Priccha:</b> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li></ul><h4>B. The Samhitas and Puranas</h4><ul><li><b>Brihat Samhita (by Varahamihira):</b> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li><li><b>Vishnudharmottara Purana:</b> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li><li><b>Agni Purana & Matsya Purana:</b> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li></ul><h4>C. The Agamas (The Living Codes of the Temple City)</h4><ul><li><b>Kamikagama, Karanagama, and Suprabhedagama:</b> In South India, the Agamas are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the Prakaras (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</li></ul><h3>The Blueprint: How the 'Divine Reality' is Built</h3><p>According to these texts, a divine city is built using the Vastu Purusha Mandala. For a major city, a grid of 81 squares (9x9), known as the <b>Paramasayika mandala</b>, is drawn on the earth.</p><ul><li><b>The Brahmasthana (The Divine Center):</b> The central squares of the grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple. This is the anchor of the city.</li><li><b>The Prakaras (The Concentric Layers):</b> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li><li><b>The Zoning of Samsara (Worldly Life):</b><ul><li><i>Inner Ring:</i> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li><li><i>Middle Ring:</i> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the engine of society).</li><li><i>Outer Ring:</i> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li><li><i>The Periphery:</i> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li></ul></li></ul><h3>The Ultimate Example: Madurai Sthalam</h3><p>Madurai is the flawless, living embodiment of the Mayamatam and the Agamas. It is known in the texts as a <b>Padma Vana</b> (Lotus Forest) or <b>Kudal</b> (The Confluence).</p><ul><li><b>The Center (The Pistil of the Lotus):</b> At the absolute Brahmasthana sits the Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless Consciousness, and Shakti (Meenakshi) represents the dynamic Energy of the universe. They are the still point of the turning world.</li><li><b>The Streets (The Petals of the Lotus):</b> Radiating outward from the temple are concentric rectangular streets, named after the Tamil months: Chitrai Veedhi (Innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (Outermost).</li><li><b>The Transformation of Samsara into Dharma:</b> In a modern city, the center is usually a bank, a mall, or a corporate plaza (representing greed and commerce). In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing Pradakshina (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce of the outer streets is protected and sanctified by the stillness of the inner sanctum.</li><li><b>The Water Element:</b> The texts demand a water body for purification. Madurai is built on the banks of the Vaigai River, and the temple itself houses the Potramarai Kulam (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality).</li></ul><h3>Summary: Environment Dictates Consciousness</h3><p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: Environment dictates consciousness. If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara gets, is always held in the loving, gravitational embrace of the Divine.</p>"""
    
    new_content = content[:str_start] + new_body + content[str_end:]
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("  [SUCCESS] Updated server.py")

replace_wisdom_hub()
replace_server()
