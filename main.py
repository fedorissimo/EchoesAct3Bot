from selenium import webdriver

# Launch WhatsApp Web
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

# Wait for user to log in and select a group chat
input("Please scan the QR code and select a group chat, then press Enter to continue...")

# Infinite loop to continuously read new messages
while True:
    # Find all messages that haven't been read yet
    unread_msgs = driver.find_elements_by_xpath("//div[@class='_1GlEs'][not(contains(@class, '_38M1B'))]//span[@class='selectable-text invisible-space copyable-text']")

    # Print each message's text and sender
    for msg in unread_msgs:
        sender = driver.find_element_by_xpath("//div[@class='_1GlEs'][contains(@class, '_19RFN')]/div/div/div/span[@class='_17zMk']")
        print(f"{sender.text}: {msg.text}")
        msg.click()

    # Wait to read new messages
    driver.implicitly_wait(1)