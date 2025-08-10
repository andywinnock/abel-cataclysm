package com.github.L_Ender.cataclysm.entity.Pet;

import com.github.L_Ender.cataclysm.Cataclysm;
import com.github.L_Ender.cataclysm.config.CMConfig;
import com.github.L_Ender.cataclysm.entity.Pet.AI.InternalPetStateGoal;
import com.github.L_Ender.cataclysm.entity.Pet.AI.TameableAIFollowOwner;
import com.github.L_Ender.cataclysm.entity.etc.SmartBodyHelper2;
import com.github.L_Ender.cataclysm.init.ModItems;
import com.github.L_Ender.cataclysm.init.ModSounds;
import com.github.L_Ender.cataclysm.init.ModTag;
import com.github.L_Ender.cataclysm.inventory.SeedotMenu;
import com.github.L_Ender.cataclysm.message.MessageSeedotInventory;
import net.minecraft.advancements.CriteriaTriggers;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.*;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.BodyRotationControl;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.animal.Bucketable;
import net.minecraft.world.entity.animal.Wolf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.entity.player.PlayerContainerEvent;
import net.minecraftforge.network.PacketDistributor;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import java.util.Optional;

public class Seedot_Entity extends InternalAnimationPet implements Bucketable, ContainerListener, HasCustomInventoryScreen {
    private static final EntityDataAccessor<Boolean> FROM_BUCKET = SynchedEntityData.defineId(Seedot_Entity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> IS_SITTING = SynchedEntityData.defineId(Seedot_Entity.class, EntityDataSerializers.BOOLEAN);
    public SimpleContainer seedotInventory;
    public AnimationState idleAnimationState = new AnimationState();
    public AnimationState walkAnimationState = new AnimationState();
    public AnimationState sitAnimationState = new AnimationState();

    public Seedot_Entity(EntityType<? extends Seedot_Entity> type, Level world) {
        super(type, world);
        this.createInventory();
        this.xpReward = 0;
        setConfigattribute(this, CMConfig.MinistrosityHealthMultiplier, 1);
        this.setMaxUpStep(1.0F);
        // Infinite health
        this.getAttribute(Attributes.MAX_HEALTH).setBaseValue(Float.MAX_VALUE);
        this.setHealth(Float.MAX_VALUE);
    }

    protected void registerGoals() {
        this.goalSelector.addGoal(0, new SitWhenOrderedToGoal(this));
        this.goalSelector.addGoal(6, new TameableAIFollowOwner(this, 1.3D, 6.0F, 2.0F, true));
        this.goalSelector.addGoal(6, new TemptGoal(this, 1.0D, Ingredient.of(Items.WHEAT_SEEDS), false));
        this.goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        this.goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 6.0F));
        this.goalSelector.addGoal(7, new RandomStrollGoal(this, 1.0D, 60));
        this.goalSelector.addGoal(1, new InternalPetStateGoal(this, 1, 1, 0, 0, 0) {
            @Override
            public boolean canUse() {
                return super.canUse();
            }

            @Override
            public void tick() {
                entity.setDeltaMovement(0, entity.getDeltaMovement().y, 0);
            }
        });
    }

    @Override
    public boolean hurt(DamageSource pDamageSource, float pDamageAmount) {
        // Infinite health - cannot be hurt
        return false;
    }

    @Override
    public boolean isInvulnerableTo(DamageSource pDamageSource) {
        return true;
    }

    protected SoundEvent getHurtSound(DamageSource damageSourceIn) {
        return SoundEvents.GRASS_BREAK;
    }

    protected SoundEvent getDeathSound() {
        return SoundEvents.GRASS_BREAK;
    }

    protected SoundEvent getAmbientSound() {
        return SoundEvents.GRASS_STEP;
    }

    public void setIsSitting(boolean isSitting) {
        this.entityData.set(IS_SITTING, isSitting);
    }

    public boolean getIsSitting() {
        return this.entityData.get(IS_SITTING);
    }

    protected int getInventorySize() {
        return 17;
    }

    protected void createInventory() {
        SimpleContainer simplecontainer = this.seedotInventory;
        this.seedotInventory = new SimpleContainer(this.getInventorySize());
        if (simplecontainer != null) {
            simplecontainer.removeListener(this);
            int i = Math.min(simplecontainer.getContainerSize(), this.seedotInventory.getContainerSize());

            for (int j = 0; j < i; ++j) {
                ItemStack itemstack = simplecontainer.getItem(j);
                if (!itemstack.isEmpty()) {
                    this.seedotInventory.setItem(j, itemstack.copy());
                }
            }
        }

        this.seedotInventory.addListener(this);
        this.itemHandler = net.minecraftforge.common.util.LazyOptional.of(() -> new net.minecraftforge.items.wrapper.InvWrapper(this.seedotInventory));
    }

    @Override
    public void openCustomInventoryScreen(Player playerEntity) {
        if (playerEntity instanceof ServerPlayer serverplayer) {
            if (isAlive()) {
                if (serverplayer.containerMenu != serverplayer.inventoryMenu) {
                    serverplayer.closeContainer();
                }

                serverplayer.nextContainerCounter();
                Cataclysm.NETWORK_WRAPPER.send(PacketDistributor.PLAYER.with(() -> serverplayer), new MessageSeedotInventory(serverplayer.containerCounter, this.seedotInventory.getContainerSize(), this.getId()));
                serverplayer.containerMenu = new SeedotMenu(serverplayer.containerCounter, serverplayer.getInventory(), this.seedotInventory, this);
                serverplayer.initMenu(serverplayer.containerMenu);
                MinecraftForge.EVENT_BUS.post(new PlayerContainerEvent.Open(serverplayer, serverplayer.containerMenu));
            }
        }
    }

    public int getInventoryColumns() {
        return 5;
    }

    public void containerChanged(Container p_30548_) {
    }

    public AnimationState getAnimationState(String input) {
        switch (input) {
            case "idle":
                return this.idleAnimationState;
            case "walk":
                return this.walkAnimationState;
            case "sit":
                return this.sitAnimationState;
            default:
                return this.idleAnimationState;
        }
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, Float.MAX_VALUE)
                .add(Attributes.MOVEMENT_SPEED, 0.25F)
                .add(Attributes.FOLLOW_RANGE, 48.0D);
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack itemstack = player.getItemInHand(hand);
        Item item = itemstack.getItem();

        if (this.level().isClientSide) {
            boolean flag = this.isOwnedBy(player) || this.isTame() || (item == Items.WHEAT_SEEDS && !this.isTame());
            return flag ? InteractionResult.CONSUME : InteractionResult.PASS;
        } else {
            if (this.isTame()) {
                if (this.isFood(itemstack) && this.getHealth() < this.getMaxHealth()) {
                    if (!player.getAbilities().instabuild) {
                        itemstack.shrink(1);
                    }
                    this.heal(1.0F);
                    this.gameEvent(GameEvent.EAT, this);
                    return InteractionResult.SUCCESS;
                }

                if (this.isOwnedBy(player) && !this.isFood(itemstack)) {
                    if (!player.isShiftKeyDown()) {
                        this.openCustomInventoryScreen(player);
                        this.setCommand(2);
                        this.setOrderedToSit(true);
                        return InteractionResult.sidedSuccess(this.level().isClientSide);
                    }
                }
            } else if (item == Items.WHEAT_SEEDS) {
                if (!player.getAbilities().instabuild) {
                    itemstack.shrink(1);
                }

                if (this.random.nextInt(3) == 0) {
                    this.tame(player);
                    this.navigation.stop();
                    this.setTarget(null);
                    this.setOrderedToSit(true);
                    this.level().broadcastEntityEvent(this, (byte) 7);
                } else {
                    this.level().broadcastEntityEvent(this, (byte) 6);
                }

                return InteractionResult.SUCCESS;
            }

            InteractionResult interactionresult = itemstack.interactLivingEntity(player, this, hand);
            if (interactionresult != InteractionResult.SUCCESS && isTame() && isOwnedBy(player)) {
                if (player.isShiftKeyDown()) {
                    this.setCommand(this.getCommand() + 1);
                    if (this.getCommand() == 3) {
                        this.setCommand(0);
                    }
                    player.displayClientMessage(Component.translatable("entity.cataclysm.all.command_" + this.getCommand(), this.getName()), true);
                    boolean sit = this.getCommand() == 2;
                    if (sit) {
                        this.setOrderedToSit(true);
                        return InteractionResult.SUCCESS;
                    } else {
                        this.setOrderedToSit(false);
                        return InteractionResult.SUCCESS;
                    }
                }
            }
            return super.mobInteract(player, hand);
        }
    }


    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(Items.WHEAT_SEEDS);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(FROM_BUCKET, false);
        this.entityData.define(IS_SITTING, false);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag compound) {
        super.addAdditionalSaveData(compound);
        compound.putBoolean("FromBucket", this.fromBucket());
        compound.putBoolean("IsSitting", this.getIsSitting());
        
        if (this.seedotInventory != null) {
            ListTag listtag = new ListTag();
            for (int i = 0; i < this.seedotInventory.getContainerSize(); ++i) {
                ItemStack itemstack = this.seedotInventory.getItem(i);
                if (!itemstack.isEmpty()) {
                    CompoundTag compoundtag = new CompoundTag();
                    compoundtag.putByte("Slot", (byte) i);
                    itemstack.save(compoundtag);
                    listtag.add(compoundtag);
                }
            }
            compound.put("Items", listtag);
        }
    }

    @Override
    public void readAdditionalSaveData(CompoundTag compound) {
        super.readAdditionalSaveData(compound);
        this.setFromBucket(compound.getBoolean("FromBucket"));
        this.setIsSitting(compound.getBoolean("IsSitting"));
        
        if (this.seedotInventory != null) {
            ListTag listtag = compound.getList("Items", 10);
            for (int i = 0; i < listtag.size(); ++i) {
                CompoundTag compoundtag = listtag.getCompound(i);
                int j = compoundtag.getByte("Slot") & 255;
                if (j >= 0 && j < this.seedotInventory.getContainerSize()) {
                    this.seedotInventory.setItem(j, ItemStack.of(compoundtag));
                }
            }
        }
    }

    @Override
    public boolean fromBucket() {
        return this.entityData.get(FROM_BUCKET);
    }

    @Override
    public void setFromBucket(boolean fromBucket) {
        this.entityData.set(FROM_BUCKET, fromBucket);
    }

    @Override
    public void saveToBucketTag(ItemStack bucket) {
        Bucketable.saveDefaultDataToBucketTag(this, bucket);
    }

    @Override
    public void loadFromBucketTag(CompoundTag tag) {
        Bucketable.loadDefaultDataFromBucketTag(this, tag);
    }

    @Override
    public ItemStack getBucketItemStack() {
        return new ItemStack(Items.WATER_BUCKET);
    }

    @Override
    public SoundEvent getPickupSound() {
        return SoundEvents.BUCKET_FILL;
    }

    @Override
    protected BodyRotationControl createBodyControl() {
        return new SmartBodyHelper2(this);
    }

    @Override
    public void tick() {
        super.tick();

        if (this.level().isClientSide) {
            if (this.isOrderedToSit()) {
                this.sitAnimationState.startIfStopped(this.tickCount);
                this.idleAnimationState.stop();
                this.walkAnimationState.stop();
            } else if (this.getDeltaMovement().horizontalDistanceSqr() > 1.0E-6D) {
                this.walkAnimationState.startIfStopped(this.tickCount);
                this.idleAnimationState.stop();
                this.sitAnimationState.stop();
            } else {
                this.idleAnimationState.startIfStopped(this.tickCount);
                this.walkAnimationState.stop();
                this.sitAnimationState.stop();
            }
        }
    }

    @Override
    public boolean shouldFollow() {
        return this.getCommand() == 1;
    }

    public boolean hasInventoryChanged(Container p_149512_) {
        return this.seedotInventory != p_149512_;
    }

    private net.minecraftforge.common.util.LazyOptional<?> itemHandler = null;

    @Override
    public <T> net.minecraftforge.common.util.LazyOptional<T> getCapability(net.minecraftforge.common.capabilities.Capability<T> capability, @Nullable net.minecraft.core.Direction facing) {
        if (this.isAlive() && capability == net.minecraftforge.common.capabilities.ForgeCapabilities.ITEM_HANDLER && itemHandler != null)
            return itemHandler.cast();
        return super.getCapability(capability, facing);
    }

    @Override
    public void invalidateCaps() {
        super.invalidateCaps();
        if (itemHandler != null) {
            net.minecraftforge.common.util.LazyOptional<?> oldHandler = itemHandler;
            itemHandler = null;
            oldHandler.invalidate();
        }
    }
}