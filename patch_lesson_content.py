import re

def update_interactive_lessons():
    print("Updating interactive_lesson.html content...")
    filename = "interactive_lesson.html"
    content = open(filename, encoding="utf-8").read()
    
    # 1. vastu scientific block
    old_vastu = """      scientific: {
        title: "The Paramasayika Grid & Zoning of Samsara",
        text: "The ancient Vastu texts dictate that a divine city must be designed around the Vastu Purusha Mandala. For a major metropolis, a 9×9 grid of 81 squares, known as the Paramasayika mandala, is projected onto the earth. The absolute center of this grid is the Brahmasthana (the seat of the Creator). Considered unmanifest consciousness, this area is strictly reserved for the central temple; no mortal is permitted to reside here. Radiating outward from this spiritual anchor, the city organizes Samsara (worldly life) into concentric rectangular layers (Prakaras) transitioning from spirit to matter: the Inner Ring (Sattvic: priests, scholars, and ascetics closest to the temple), the Middle Ring (Rajasic: rulers, warriors, merchants, and artisans driving society), the Outer Ring (Tamasic: agriculture, heavy industries, and labor), and the Periphery far outside the gates where cremation grounds and polluting industries are placed to safeguard the spiritual purity of the center."
      },"""
      
    # Note: the original text from view_file has "pure, unmanifest consciousness" or "Considered unmanifest consciousness" or "Considered pure, unmanifest consciousness"? Let's double check.
    # From view_file, it is:
    # "Considered pure, unmanifest consciousness, this area is strictly reserved for the central temple; no mortal is permitted to reside here."
    # Let's perform a substring replace. We can define the old block exactly as it is in the file.
    
    # Let's read the exact old vastu block:
    old_vastu_exact = """      scientific: {
        title: "The Paramasayika Grid & Zoning of Samsara",
        text: "The ancient Vastu texts dictate that a divine city must be designed around the Vastu Purusha Mandala. For a major metropolis, a 9×9 grid of 81 squares, known as the Paramasayika mandala, is projected onto the earth. The absolute center of this grid is the Brahmasthana (the seat of the Creator). Considered pure, unmanifest consciousness, this area is strictly reserved for the central temple; no mortal is permitted to reside here. Radiating outward from this spiritual anchor, the city organizes Samsara (worldly life) into concentric rectangular layers (Prakaras) transitioning from spirit to matter: the Inner Ring (Sattvic: priests, scholars, and ascetics closest to the temple), the Middle Ring (Rajasic: rulers, warriors, merchants, and artisans driving society), the Outer Ring (Tamasic: agriculture, heavy industries, and labor), and the Periphery far outside the gates where cremation grounds and polluting industries are placed to safeguard the spiritual purity of the center."
      },"""

    new_vastu = """      scientific: {
        title: "The Paramasayika Grid & Zoning of Samsara",
        text: `
          <h3>The Sacred Texts & The Blueprint of the Vastu Purusha Mandala</h3>
          <p>According to ancient treatises, the layout of a divine city is designed as a living reflection (pratikriti) of the cosmos. For a major city, a grid of 81 squares (9x9), known as the <strong>Paramasayika Mandala</strong>, is projected onto the earth.</p>
          
          <h4>A. The Shilpa Shastras (The Architectural Manuals)</h4>
          <ul>
            <li><strong>Manasara (Manasara Shilpa Shastra):</strong> The ultimate encyclopedia of Vastu. It contains a specific section called <em>Nagara Vidhana</em> (Rules for Towns) which categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li>
            <li><strong>Mayamatam (Mayamata):</strong> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li>
            <li><strong>Samarangana Sutradhara:</strong> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li>
            <li><strong>Aparajita Priccha:</strong> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li>
          </ul>

          <h4>B. The Samhitas and Puranas</h4>
          <ul>
            <li><strong>Brihat Samhita (by Varahamihira):</strong> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li>
            <li><strong>Vishnudharmottara Purana:</strong> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li>
            <li><strong>Agni Purana & Matsya Purana:</strong> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li>
          </ul>

          <h4>The Blueprint: How the "Divine Reality" is Built</h4>
          <ul>
            <li><strong>The Brahmasthana (The Divine Center):</strong> The central squares of the 9x9 Paramasayika grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple, acting as the spiritual and physical anchor of the city.</li>
            <li><strong>The Prakaras (The Concentric Layers):</strong> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li>
            <li><strong>The Zoning of Samsara (Worldly Life):</strong>
              <ul>
                <li><em>Inner Ring:</em> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li>
                <li><em>Middle Ring:</em> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the active engine of society).</li>
                <li><em>Outer Ring:</em> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li>
                <li><em>The Periphery:</em> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li>
              </ul>
            </li>
          </ul>
        `
      },"""

    # 2. upanishads scientific block
    old_upanishads_exact = """      scientific: {
        title: "The Agamic Walls of Protection",
        text: "In the South Indian temple city model, the Agamas (Kamikagama, Karanagama, and Suprabhedagama) dictate the supreme spatial layout. The temple and its surrounding town are structured as concentric rectangular walls and streets (Prakaras). These walls act as energetic filters, shielding the central sanctum (Garbhagriha) from chaotic outer influences. This maps directly to the five-sheath (Pancha Kosha) model of human consciousness, establishing the city as a macrocosmic physical body."
      },"""

    new_upanishads = """      scientific: {
        title: "The Agamic Walls of Protection",
        text: `
          <h3>The Agamas & Dahara Vidya: The Cosmos Within and Without</h3>
          <p>The layout of the temple city is a macrocosmic physical body, externalizing the Upanishadic <em>Dahara Vidya</em>, which states that the entire universe is mirrored within the space of the human heart (Dahara Akasha).</p>
          
          <h4>C. The Agamas (The Living Codes of the Temple City)</h4>
          <p>In South India, the Agamas (like the <strong>Kamikagama</strong>, <strong>Karanagama</strong>, and <strong>Suprabhedagama</strong>) are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the <strong>Prakaras</strong> (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</p>
          
          <h4>Concentric Layers & Spiritual Correspondence</h4>
          <p>The city's walls and streets are arranged concentrically, mapping directly to the five-sheath (Pancha Kosha) model of human consciousness:</p>
          <ul>
            <li><strong>Annamaya Kosha (Material Sheath):</strong> The outermost perimeter, defensive walls, and outer city gates filtering raw, physical forces.</li>
            <li><strong>Pranamaya Kosha (Vital Sheath):</strong> The outer streets of commerce, agriculture, and civic life, where the city's energy flows.</li>
            <li><strong>Manomaya Kosha (Mental Sheath):</strong> The middle ring housing scholars, administrators, and halls of learning.</li>
            <li><strong>Vijnanamaya Kosha (Intellect/Wisdom Sheath):</strong> The inner temple enclosures and courtyards where spiritual and intellectual discourses occur.</li>
            <li><strong>Anandamaya Kosha (Bliss Sheath):</strong> The Garbhagriha (Innermost Sanctum) at the absolute Brahmasthana, holding the deity representing unmanifest consciousness.</li>
          </ul>
          <p>By passing through these successive gates and streets, a devotee is not merely walking through physical space; they are journeying inward, circumambulating the sheaths of their own consciousness.</p>
        `
      },"""

    # 3. yoga scientific block (Atharvaveda details)
    old_yoga_exact = """      scientific: {
        title: "The Knowing and Doing of the Atharvaveda",
        text: "The Atharvaveda (housing the Sthapatya Veda) is the energetic soul and protective shield of Nagara Nirmana. If the Shilpa Shastras and Agamas provide the structural blueprint (the anatomy), the Atharvaveda provides the prana (life force) that makes physical structures active. In <strong>Knowing (Wisdom)</strong>, it views the earth as a living organism with Nadis and vital energy points (Marma Sthanas) and links the microcosm to the macrocosm by balancing the five elements (Pancha Bhoota) to maintain societal harmony. In <strong>Doing (Execution)</strong>, it guides Bhoomi Pujan & Vastu Shanti (pacifying the earth; Book 3, Hymn 12 for foundation raising, invoking Tvastar), Nagara Raksha (shielding boundaries using Rakshoghna/Krivinashana hymns and cardinal gate guardians), water hydrology (temple tanks like Potramarai Kulam and Vaigai River alignment), and statecraft zoning. For physical dimensions and structural details, it hands off to Mayamatam and Agamas."
      },"""

    new_yoga = """      scientific: {
        title: "The Knowing and Doing of the Atharvaveda",
        text: `
          <h3>The Energetic Soul of Nagara Nirmana</h3>
          <p>The Atharvaveda is the energetic soul and the protective shield of Nagara Nirmana (city building). If the Shilpa Shastras (like Manasara) and the Agamas provide the geometric blueprint (the math, the measurements, and the physical execution), the Atharvaveda provides the <em>prana</em> (life force), the ritual execution, and the energetic wisdom required to make that physical structure actually "alive" and divine. Without the energetic rituals of the Atharvaveda, a city built using only the Agamas would just be a mathematically perfect, but ultimately "dead" pile of stones.</p>
          
          <h4>1. The Wisdom (The Knowing): The Earth as a Living Organism</h4>
          <ul>
            <li><strong>Vastu Purusha as a Living Entity:</strong> While the Rigveda introduces the cosmic order (Rta), the Atharvaveda grounds this into the earth. It teaches that land is not dead dirt; it is a living, breathing organism with energy meridians (Nadis), just like the human body. The Atharvaveda gives the wisdom to identify the <em>marma sthanas</em> (vital energy points) of a geographical site so that the central temple (Brahmasthana) can be placed exactly on the earth's spiritual nerve center.</li>
            <li><strong>The Microcosm-Macrocosm Link:</strong> Tying back to the body and the planets, the Atharvaveda contains the roots of Ayurveda (the science of life). Just as Ayurveda balances the five elements (Pancha Bhoota) inside the human body to prevent disease, the Sthapatya Veda of the Atharvaveda balances the five elements in the physical geography of a city to prevent societal decay, poverty, and natural disasters.</li>
            <li><strong>Vastospati (The Lord of the Dwelling):</strong> The Atharvaveda contains deep philosophical hymns dedicated to Vastospati, the deity who presides over physical spaces. It teaches the "knowing" that a house or a city is not just a shelter for humans, but a shared dwelling space for humans, nature, and divine energies.</li>
          </ul>

          <h4>2. The Execution (The Doing): Rituals, Shielding, and Statecraft</h4>
          <ul>
            <li><strong>Bhoomi Pujan and Vastu Shanti (Pacifying the Earth):</strong> Before a divine city like Madurai is built, the earth must be "asked" for permission and pacified. The Atharvaveda contains the exact mantras and rituals to heal the land of any past trauma, clear it of negative entities, and stabilize its magnetic grid. Book 3, Hymn 12 of the Atharvaveda is a famous, beautiful hymn specifically dedicated to the raising of a house's foundation, invoking the creators (Tvastar) to make the dwelling prosperous and structurally sound.</li>
            <li><strong>Nagara Raksha (Protecting the City Borders):</strong> A divine city must be protected from the chaotic, untamed energies of the wilderness (Aranya) and from human enemies. The Atharvaveda is famous for its Rakshoghna (demon-destroying) and Krivinashana (evil-destroying) hymns. The execution of building the massive outer walls and the Dwarapalakas (guardian deities) at the four cardinal gates of a temple city relies on the energetic shielding protocols found in the Atharva Veda.</li>
            <li><strong>Water Management and Prosperity:</strong> A city cannot survive without water. The Atharvaveda contains extensive mantras for invoking Parjanya (the rain deity) and ensuring the flow of subterranean water. The execution of digging the temple tanks (like the Potramarai Kulam in Madurai) and ensuring the city's alignment with rivers (like the Vaigai) is guided by the Atharvanic understanding of hydrology and earthly prosperity.</li>
            <li><strong>Statecraft and Societal Harmony:</strong> The Atharvaveda contains the roots of Arthashastra (statecraft). It provides the wisdom on how to execute the zoning of the city so that the different classes of society (priests, warriors, merchants, laborers) live in harmony without their conflicting energetic vibrations disrupting the peace of the central temple.</li>
          </ul>

          <h4>3. The Limitation: Where the Atharvaveda "Hands Off"</h4>
          <p>To understand its effectiveness, you must also understand its limits. The Atharvaveda will not tell you:</p>
          <ul>
            <li>How wide the streets (like Chitrai Veedhi in Madurai) should be in feet.</li>
            <li>The exact mathematical ratio of the temple Gopuram (tower) to the sanctum.</li>
            <li>Which specific stone to carve for the Lingam.</li>
          </ul>
          <p>For the geometric, architectural, and structural execution, the Atharvaveda hands the baton to the Agamas (like Kamikagama) and the Shilpa Shastras (like Mayamatam).</p>
          
          <p><strong>Summary (The Anesthetic vs. The Scalpel):</strong> Think of building a divine city like performing a highly complex, sacred surgery on the Earth. The Atharvaveda is the anesthetic, the life-support, and the blessing. It purifies the site, protects the borders from negative forces, aligns the elemental energies, and invites the divine presence into the soil. It provides the spiritual execution. The Agamas and Shilpa Shastras are the surgeon's scalpel and the anatomical charts, providing the exact measurements, the geometry of the Mandala, and the physical construction. Both are absolutely mandatory to breathe life into the physical reality.</p>
        `
      },"""

    # 4. sthapatya scientific block (Madurai details)
    old_sthapatya_exact = """      scientific: {
        title: "Madurai: The Living Lotus Geometry",
        text: "The city of Madurai is the flawless, living embodiment of the Mayamatam and Agamic urban planning. Referred to as a Padma Vana (Lotus Forest) or Kudal (Confluence), it is built as a concentric layout representing the petals of a lotus radiating from the absolute Brahmasthana. At this center stands the Meenakshi Sundareswarar Temple, where Sundareswarar (Shiva) represents pure, formless consciousness, and Meenakshi (Shakti) represents dynamic cosmic energy. Radiating outward are concentric streets named after the Tamil months: Chitrai Veedhi (innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (outermost). Because all civic life, markets, and routes wrap around the temple, citizens perform Pradakshina (spiritual circumambulation) simply by walking through their daily lives, ensuring that Samsara physically revolves around the Divine. The water element is anchored by the Vaigai River and the temple's Potramarai Kulam (Golden Lotus Tank), which served as the seat of the Tamil Sangam."
      },"""

    new_sthapatya = """      scientific: {
        title: "Madurai: The Living Lotus Geometry",
        text: `
          <h3>Madurai Sthalam: The Flawless Lotus City</h3>
          <p>Madurai is the living, breathing embodiment of the <em>Mayamatam</em> and the <em>Agamas</em>. In ancient texts, it is referred to as a <strong>Padma Vana</strong> (Lotus Forest) or <strong>Kudal</strong> (The Confluence), built in a layout that mirrors a blooming lotus.</p>
          
          <h4>The Center (The Pistil of the Lotus)</h4>
          <p>At the absolute Brahmasthana sits the <strong>Meenakshi Sundareswarar Temple</strong>. Sundareswarar (Shiva) represents pure, formless Consciousness, and Meenakshi (Shakti) represents the dynamic Energy of the universe. Together, they act as the still point of the turning world, the spiritual anchor of the entire metropolis.</p>
          
          <h4>The Concentric Streets (The Petals of the Lotus)</h4>
          <p>Radiating outward from the temple are concentric rectangular streets, named after the Tamil months:</p>
          <ul>
            <li><strong>Chitrai Veedhi</strong> (Innermost, closest to the temple)</li>
            <li><strong>Aavani Moola Veedhi</strong> (Middle ring of administrative power)</li>
            <li><strong>Masi Veedhi</strong> (Commercial and residential hub)</li>
            <li><strong>Aadi Veedhi</strong> (Outermost ring, border boundaries)</li>
          </ul>

          <h4>The Transformation of Samsara into Dharma</h4>
          <p>In a modern city, the center is usually a bank, a mall, or a corporate plaza, representing greed and commerce. In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing <strong>Pradakshina</strong> (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce and activity of the outer streets are protected and sanctified by the stillness of the inner sanctum.</p>

          <h4>The Water Element</h4>
          <p>The texts demand a water body for purification. Madurai is built on the banks of the <strong>Vaigai River</strong>, and the temple itself houses the <strong>Potramarai Kulam</strong> (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality), providing physical, intellectual, and spiritual purification.</p>

          <h4>Summary: Environment Dictates Consciousness</h4>
          <p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: <strong>Environment dictates consciousness.</strong> If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara (worldly life) gets, is always held in the loving, gravitational embrace of the Divine.</p>
        `
      },"""

    replacements = [
        (old_vastu_exact, new_vastu),
        (old_upanishads_exact, new_upanishads),
        (old_yoga_exact, new_yoga),
        (old_sthapatya_exact, new_sthapatya)
    ]
    
    for idx, (old_p, new_p) in enumerate(replacements, 1):
        if old_p in content:
            content = content.replace(old_p, new_p)
            print(f"  [SUCCESS] Replaced block {idx}")
        else:
            print(f"  [ERROR] Block {idx} NOT found in interactive_lesson.html")
            
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def update_wisdom_hub_article():
    print("Updating wisdom_hub.html Article 4...")
    filename = "wisdom_hub.html"
    content = open(filename, encoding="utf-8").read()
    
    # Locate Article 4 block
    old_article_4_content = """content: '<h3>The Texts of Nagara Nirmana</h3><p>The layout and development of divine settlements in India are codified in the Shilpa Shastras (such as the <i>Manasara</i>, <i>Mayamatam</i>, <i>Samarangana Sutradhara</i>, and <i>Aparajita Priccha</i>), the Samhitas and Puranas (like Varahamihira\'s <i>Brihat Samhita</i> and the <i>Vishnudharmottara Purana</i>), and the Agamas (including the <i>Kamikagama</i>). These texts dictate that the physical environment directly governs human consciousness, mandating that the city structure must serve as a living reflection (pratikriti) of the cosmos.</p><h3>The Blueprint of the Vastu Purusha Mandala</h3><p>For a major city, a 9x9 grid of 81 squares, known as the <b>Paramasayika Mandala</b>, is drawn on the earth. At the absolute center sits the <b>Brahmasthana</b>\\u2014the seat of the Creator. Reserved exclusively for the temple, no mortal is allowed to reside here, establishing the Divine as the city\'s spiritual anchor. The city spreads outward in concentric rectangular layers (Prakaras) representing the descending sheaths of spirit into matter: the Inner Ring (Sattvic: scholars and ascetics), the Middle Ring (Rajasic: rulers and merchants), the Outer Ring (Tamasic: labor and agriculture), and the Periphery far outside (polluting industries like tanneries, ensuring the center\'s purity).</p><h3>Madurai: The Living Lotus City</h3><p>Madurai stands as the ultimate living embodiment of the Mayamatam and Agamic layout. Known in the shastras as a <b>Padma Vana</b> (Lotus Forest) or Kudal, the city represents the petals of a lotus radiating from the central Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless consciousness, and Shakti (Meenakshi) represents dynamic energy. The concentric streets are named after the Tamil months: Chitrai, Aavani Moola, Masi, and Aadi Veedhi. Because these streets wrap around the temple, every daily activity performs circumambulation (Pradakshina) of God. The Vaigai River and Potramarai Kulam (Golden Lotus Tank) provide physical and spiritual purification, making Madurai the flawless synthesis of civic life and sacred geometry.</p>',"""
    
    # We will expand it to include all the details of the samhitas and paragraphs from the user
    new_article_4_content = """content: '<h3>The Sacred Texts of Nagara Nirmana</h3><p>While the term \"Samhita\" broadly refers to compendiums or collections of knowledge, the rules for building a divine city are found across Shilpa Shastras (architectural manuals), Agamas (temple and societal codes), and Puranic Samhitas.</p><h4>A. The Shilpa Shastras (The Architectural Manuals)</h4><ul><li><b>Manasara (Manasara Shilpa Shastra):</b> This is the ultimate encyclopedia of Vastu. It contains a specific section called Nagara Vidhana (Rules for Towns). It categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li><li><b>Mayamatam (Mayamata):</b> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li><li><b>Samarangana Sutradhara:</b> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li><li><b>Aparajita Priccha:</b> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li></ul><h4>B. The Samhitas and Puranas</h4><ul><li><b>Brihat Samhita (by Varahamihira):</b> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li><li><b>Vishnudharmottara Purana:</b> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li><li><b>Agni Purana & Matsya Purana:</b> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li></ul><h4>C. The Agamas (The Living Codes of the Temple City)</h4><ul><li><b>Kamikagama, Karanagama, and Suprabhedagama:</b> In South India, the Agamas are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the Prakaras (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</li></ul><h3>The Blueprint: How the \"Divine Reality\" is Built</h3><p>According to these texts, a divine city is built using the Vastu Purusha Mandala. For a major city, a grid of 81 squares (9x9), known as the <b>Paramasayika mandala</b>, is drawn on the earth.</p><ul><li><b>The Brahmasthana (The Divine Center):</b> The central squares of the grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple. This is the anchor of the city.</li><li><b>The Prakaras (The Concentric Layers):</b> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li><li><b>The Zoning of Samsara (Worldly Life):</b><ul><li><i>Inner Ring:</i> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li><li><i>Middle Ring:</i> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the engine of society).</li><li><i>Outer Ring:</i> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li><li><i>The Periphery:</i> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li></ul></li></ul><h3>The Ultimate Example: Madurai Sthalam</h3><p>Madurai is the flawless, living embodiment of the Mayamatam and the Agamas. It is known in the texts as a <b>Padma Vana</b> (Lotus Forest) or <b>Kudal</b> (The Confluence).</p><ul><li><b>The Center (The Pistil of the Lotus):</b> At the absolute Brahmasthana sits the Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless Consciousness, and Shakti (Meenakshi) represents the dynamic Energy of the universe. They are the still point of the turning world.</li><li><b>The Streets (The Petals of the Lotus):</b> Radiating outward from the temple are concentric rectangular streets, named after the Tamil months: Chitrai Veedhi (Innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (Outermost).</li><li><b>The Transformation of Samsara into Dharma:</b> In a modern city, the center is usually a bank, a mall, or a corporate plaza (representing greed and commerce). In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing Pradakshina (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce of the outer streets is protected and sanctified by the stillness of the inner sanctum.</li><li><b>The Water Element:</b> The texts demand a water body for purification. Madurai is built on the banks of the Vaigai River, and the temple itself houses the Potramarai Kulam (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality).</li></ul><h3>Summary: Environment Dictates Consciousness</h3><p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: Environment dictates consciousness. If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara gets, is always held in the loving, gravitational embrace of the Divine.</p>',"""
    
    if old_article_4_content in content:
        content = content.replace(old_article_4_content, new_article_4_content)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [SUCCESS] Patched wisdom_hub.html Article 4")
    else:
        # Check with simple escaping difference
        escaped_old_content = old_article_4_content.replace("\\u2014", "—")
        if escaped_old_content in content:
            content = content.replace(escaped_old_content, new_article_4_content)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print("  [SUCCESS] Patched wisdom_hub.html Article 4 (escaped dash fallback)")
        else:
            print("  [ERROR] Article 4 content not matched in wisdom_hub.html")

def update_server_article():
    print("Updating server.py Article 4...")
    filename = "server.py"
    content = open(filename, encoding="utf-8").read()
    
    # Locate default_articles in server.py
    # We will replace the article with title: "The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built"
    # Let's search for the exact tuple in server.py
    
    old_server_part = """            (
                "research",
                "The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built",
                "Siddha Council",
                "A deep dive into the Vastu Purusha Mandala, the 9x9 Paramasayika grid, and the living lotus geometry of Madurai Sthalam.",
                "<h3>The Texts of Nagara Nirmana</h3><p>The layout and development of divine settlements in India are codified in the Shilpa Shastras (such as the <i>Manasara</i>, <i>Mayamatam</i>, <i>Samarangana Sutradhara</i>, and <i>Aparajita Priccha</i>), the Samhitas and Puranas (like Varahamihira\'s <i>Brihat Samhita</i> and the <i>Vishnudharmottara Purana</i>), and the Agamas (including the <i>Kamikagama</i>). These texts dictate that the physical environment directly governs human consciousness, mandating that the city structure must serve as a living reflection (pratikriti) of the cosmos.</p><h3>The Blueprint of the Vastu Purusha Mandala</h3><p>For a major city, a 9x9 grid of 81 squares, known as the <b>Paramasayika Mandala</b>, is drawn on the earth. At the absolute center sits the <b>Brahmasthana</b>\\u2014the seat of the Creator. Reserved exclusively for the temple, no mortal is allowed to reside here, establishing the Divine as the city\'s spiritual anchor. The city spreads outward in concentric rectangular layers (Prakaras) representing the descending sheaths of spirit into matter: the Inner Ring (Sattvic: scholars and ascetics), the Middle Ring (Rajasic: rulers and merchants), the Outer Ring (Tamasic: labor and agriculture), and the Periphery far outside (polluting industries like tanneries, ensuring the center\'s purity).</p><h3>Madurai: The Living Lotus City</h3><p>Madurai stands as the ultimate living embodiment of the Mayamatam and Agamic layout. Known in the shastras as a <b>Padma Vana</b> (Lotus Forest) or Kudal, the city represents the petals of a lotus radiating from the central Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless consciousness, and Shakti (Meenakshi) represents dynamic energy. The concentric streets are named after the Tamil months: Chitrai, Aavani Moola, Masi, and Aadi Veedhi. Because these streets wrap around the temple, every daily activity performs circumambulation (Pradakshina) of God. The Vaigai River and Potramarai Kulam (Golden Lotus Tank) provide physical and spiritual purification, making Madurai the flawless synthesis of civic life and sacred geometry.</p>",
                "sacred_city.png",
                now_str
            ),"""

    new_server_part = """            (
                "research",
                "The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built",
                "Siddha Council",
                "A deep dive into the Vastu Purusha Mandala, the 9x9 Paramasayika grid, and the living lotus geometry of Madurai Sthalam.",
                "<h3>The Sacred Texts of Nagara Nirmana</h3><p>While the term \\"Samhita\\" broadly refers to compendiums or collections of knowledge, the rules for building a divine city are found across Shilpa Shastras (architectural manuals), Agamas (temple and societal codes), and Puranic Samhitas.</p><h4>A. The Shilpa Shastras (The Architectural Manuals)</h4><ul><li><b>Manasara (Manasara Shilpa Shastra):</b> This is the ultimate encyclopedia of Vastu. It contains a specific section called Nagara Vidhana (Rules for Towns). It categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li><li><b>Mayamatam (Mayamata):</b> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li><li><b>Samarangana Sutradhara:</b> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li><li><b>Aparajita Priccha:</b> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li></ul><h4>B. The Samhitas and Puranas</h4><ul><li><b>Brihat Samhita (by Varahamihira):</b> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li><li><b>Vishnudharmottara Purana:</b> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li><li><b>Agni Purana & Matsya Purana:</b> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li></ul><h4>C. The Agamas (The Living Codes of the Temple City)</h4><ul><li><b>Kamikagama, Karanagama, and Suprabhedagama:</b> In South India, the Agamas are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the Prakaras (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</li></ul><h3>The Blueprint: How the \\"Divine Reality\\" is Built</h3><p>According to these texts, a divine city is built using the Vastu Purusha Mandala. For a major city, a grid of 81 squares (9x9), known as the <b>Paramasayika mandala</b>, is drawn on the earth.</p><ul><li><b>The Brahmasthana (The Divine Center):</b> The central squares of the grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple. This is the anchor of the city.</li><li><b>The Prakaras (The Concentric Layers):</b> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li><li><b>The Zoning of Samsara (Worldly Life):</b><ul><li><i>Inner Ring:</i> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li><li><i>Middle Ring:</i> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the engine of society).</li><li><i>Outer Ring:</i> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li><li><i>The Periphery:</i> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li></ul></li></ul><h3>The Ultimate Example: Madurai Sthalam</h3><p>Madurai is the flawless, living embodiment of the Mayamatam and the Agamas. It is known in the texts as a <b>Padma Vana</b> (Lotus Forest) or <b>Kudal</b> (The Confluence).</p><ul><li><b>The Center (The Pistil of the Lotus):</b> At the absolute Brahmasthana sits the Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless Consciousness, and Shakti (Meenakshi) represents the dynamic Energy of the universe. They are the still point of the turning world.</li><li><b>The Streets (The Petals of the Lotus):</b> Radiating outward from the temple are concentric rectangular streets, named after the Tamil months: Chitrai Veedhi (Innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (Outermost).</li><li><b>The Transformation of Samsara into Dharma:</b> In a modern city, the center is usually a bank, a mall, or a corporate plaza (representing greed and commerce). In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing Pradakshina (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce of the outer streets is protected and sanctified by the stillness of the inner sanctum.</li><li><b>The Water Element:</b> The texts demand a water body for purification. Madurai is built on the banks of the Vaigai River, and the temple itself houses the Potramarai Kulam (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality).</li></ul><h3>Summary: Environment Dictates Consciousness</h3><p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: Environment dictates consciousness. If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara gets, is always held in the loving, gravitational embrace of the Divine.</p>",
                "sacred_city.png",
                now_str
            ),"""

    if old_server_part in content:
        content = content.replace(old_server_part, new_server_part)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [SUCCESS] Patched server.py Article 4")
    else:
        # Check with simple escaping difference
        escaped_old_part = old_server_part.replace("\\u2014", "—")
        if escaped_old_part in content:
            content = content.replace(escaped_old_part, new_server_part)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print("  [SUCCESS] Patched server.py Article 4 (escaped dash fallback)")
        else:
            # Let's search by locating the title and substituting the content part
            print("  [ERROR] Article 4 content not matched in server.py")

update_interactive_lessons()
update_wisdom_hub_article()
update_server_article()
